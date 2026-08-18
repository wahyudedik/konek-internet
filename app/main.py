import time
import uuid
import logging
from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.routers import dns, domain, ssl, website, ip, cdn, batch, compare
from app.routers import tools_v2
from app.routers import auth, keys, workspace, notifications, ddns
from app.scheduler.jobs import scheduler
from app.utils.rate_limit import check_rate_limit, get_client_ip, get_remaining_requests
from app.data.education import EDUCATION_DATA
from app.data.faq_data import FAQ_DATA
from app.utils.validators import get_tool_meta
from app.database import init_db, close_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("konektivitas")

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============ LIFECYCLE (Database Init) ============

@app.on_event("startup")
async def startup_event():
    """Initialize database and scheduler on application startup."""
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully.")
    
    # Start monitoring scheduler
    logger.info("Starting monitoring scheduler...")
    await scheduler.start()
    logger.info("Monitoring scheduler started.")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Stopping monitoring scheduler...")
    await scheduler.stop()
    logger.info("Closing database connections...")
    await close_db()
    logger.info("Application shutdown complete.")


# ============ MIDDLEWARE ============

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())[:8]
        
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error("[%s] Request error: %s %s - %s", request_id, request.method, request.url.path, str(e))
            raise
        
        process_time = round((time.time() - start_time) * 1000, 2)
        
        # Request ID for tracing
        response.headers["X-Request-ID"] = request_id
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none';"
        
        # Performance header
        response.headers["X-Process-Time"] = f"{process_time}ms"
        
        # HSTS for production (only when HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Cache-Control for API responses
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        
        # Cache-Control for static assets
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=86400, stale-while-revalidate=604800"

        # Log slow requests (> 1 second)
        if process_time > 1000:
            logger.warning("Slow request: %s %s - %dms", request.method, request.url.path, process_time)
        
        # Log API requests
        if request.url.path.startswith("/api/"):
            logger.info("[%s] %s %s %s - %dms %s", request_id, request.client.host if request.client else "?", request.method, request.url.path, response.status_code, f"{process_time}ms")
        
        return response


app.add_middleware(SecurityHeadersMiddleware)


# Track server start time for uptime
_server_start_time = time.time()

# Rate Limiting Middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip rate limiting for non-API routes
        skip_paths = ["/docs", "/redoc", "/static", "/health", "/openapi", "/robots.txt", "/sitemap.xml"]
        if any(path.startswith(p) or path == p for p in skip_paths):
            return await call_next(request)
        
        # Only rate limit API endpoints
        if path.startswith("/api/"):
            ip = get_client_ip(request)
            if not check_rate_limit(ip):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Coba lagi dalam 1 menit.", "retry_after": 60},
                    headers={
                        "X-RateLimit-Limit": "60",
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + 60),
                        "Retry-After": "60",
                    }
                )
        
        response = await call_next(request)
        
        # Add rate limit headers for API
        if path.startswith("/api/"):
            ip = get_client_ip(request)
            remaining = get_remaining_requests(ip)
            response.headers["X-RateLimit-Limit"] = "60"
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        
        return response


app.add_middleware(RateLimitMiddleware)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")


# Category URL mapping for breadcrumb links
CATEGORY_MAP = {
    "DNS": "/?category=dns",
    "Domain": "/?category=domain",
    "SSL": "/?category=ssl",
    "Website": "/?category=website",
    "IP": "/?category=ip",
}


def template_response(template_name: str, request: Request, **kwargs) -> Response:
    """Helper to build template response with consistent context (faqs for JSON-LD)"""
    context = {"request": request, "faqs": FAQ_DATA}
    context.update(kwargs)
    return templates.TemplateResponse(template_name, context)


def tool_context(request: Request, title: str, tool_key: str, extra: dict = None) -> dict:
    """Build template context for tool pages with metadata, category_url, and faqs"""
    meta = get_tool_meta(tool_key)
    category_url = CATEGORY_MAP.get(meta.get("category", ""), "")
    ctx = {
        "request": request,
        "title": title,
        "meta": meta,
        "edu_data": EDUCATION_DATA.get(tool_key, {}),
        "category_url": category_url,
        "faqs": FAQ_DATA,
    }
    if extra:
        ctx.update(extra)
    return ctx

# API routers — Public Tools (Fase 1)
app.include_router(dns.router, prefix="/api/v1", tags=["DNS"])
app.include_router(domain.router, prefix="/api/v1", tags=["Domain"])
app.include_router(ssl.router, prefix="/api/v1", tags=["SSL"])
app.include_router(website.router, prefix="/api/v1", tags=["Website"])
app.include_router(ip.router, prefix="/api/v1", tags=["IP"])
app.include_router(cdn.router, prefix="/api/v1", tags=["CDN"])
app.include_router(batch.router, prefix="/api/v1", tags=["Batch"])
app.include_router(compare.router, prefix="/api/v1", tags=["Compare"])

# API routers — Auth, Keys, Workspace, Notifications (Fase 2)
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(keys.router, prefix="/api/v1", tags=["API Keys"])
app.include_router(workspace.router, prefix="/api/v1", tags=["Workspace"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notifications"])

# API routers — New Tools Fase 2
app.include_router(tools_v2.router, prefix="/api/v1", tags=["Tools v2"])

# API routers — Dynamic DNS (Fase 2)
app.include_router(ddns.router, prefix="/api/v1", tags=["Dynamic DNS"])


# ============ PAGE ROUTES ============

@app.get("/")
async def homepage(request: Request):
    return template_response("index.html", request, title="Beranda", meta=None)


@app.get("/about")
async def about_page(request: Request):
    return template_response("about.html", request, title="Tentang Konektivitas.com", meta=None)


@app.get("/api-docs")
async def api_docs_page(request: Request):
    return template_response("api_docs.html", request, title="API Documentation - Konektivitas.com", meta=None)


@app.get("/dns-lookup")
async def page_dns_lookup(request: Request):
    return templates.TemplateResponse("tools/dns_lookup.html", tool_context(request, "DNS Lookup", "dns_lookup"))


@app.get("/reverse-dns")
async def page_reverse_dns(request: Request):
    return templates.TemplateResponse("tools/reverse_dns.html", tool_context(request, "Reverse DNS", "reverse_dns"))


@app.get("/dns-propagation")
async def page_dns_propagation(request: Request):
    return templates.TemplateResponse("tools/dns_propagation.html", tool_context(request, "DNS Propagation Checker", "dns_propagation"))


@app.get("/mx-lookup")
async def page_mx_lookup(request: Request):
    return templates.TemplateResponse("tools/mx_lookup.html", tool_context(request, "MX Lookup", "mx_lookup"))


@app.get("/txt-lookup")
async def page_txt_lookup(request: Request):
    return templates.TemplateResponse("tools/txt_lookup.html", tool_context(request, "TXT Lookup", "txt_lookup"))


@app.get("/cname-lookup")
async def page_cname_lookup(request: Request):
    return templates.TemplateResponse("tools/cname_lookup.html", tool_context(request, "CNAME Lookup", "cname_lookup"))


@app.get("/spf-checker")
async def page_spf_checker(request: Request):
    return templates.TemplateResponse("tools/spf_checker.html", tool_context(request, "SPF Checker", "spf_checker"))


@app.get("/dmarc-checker")
async def page_dmarc_checker(request: Request):
    return templates.TemplateResponse("tools/dmarc_checker.html", tool_context(request, "DMARC Checker", "dmarc_checker"))


@app.get("/whois-lookup")
async def page_whois_lookup(request: Request):
    return templates.TemplateResponse("tools/whois_lookup.html", tool_context(request, "WHOIS Lookup", "whois_lookup"))


@app.get("/domain-expiry")
async def page_domain_expiry(request: Request):
    return templates.TemplateResponse("tools/domain_expiry.html", tool_context(request, "Domain Expiry Checker", "domain_expiry"))


@app.get("/ssl-checker")
async def page_ssl_checker(request: Request):
    return templates.TemplateResponse("tools/ssl_checker.html", tool_context(request, "SSL Checker", "ssl_checker"))


@app.get("/ssl-expiry")
async def page_ssl_expiry(request: Request):
    return templates.TemplateResponse("tools/ssl_expiry.html", tool_context(request, "SSL Expiry Checker", "ssl_expiry"))


@app.get("/ping-checker")
async def page_ping_checker(request: Request):
    return templates.TemplateResponse("tools/ping_checker.html", tool_context(request, "Ping Checker", "ping_checker"))


@app.get("/http-status")
async def page_http_status(request: Request):
    return templates.TemplateResponse("tools/http_status.html", tool_context(request, "HTTP Status Checker", "http_status"))


@app.get("/redirect-checker")
async def page_redirect_checker(request: Request):
    return templates.TemplateResponse("tools/redirect_checker.html", tool_context(request, "Redirect Checker", "redirect_checker"))


@app.get("/header-checker")
async def page_header_checker(request: Request):
    return templates.TemplateResponse("tools/header_checker.html", tool_context(request, "Header Checker", "header_checker"))


@app.get("/ip-lookup")
async def page_ip_lookup(request: Request):
    return templates.TemplateResponse("tools/ip_lookup.html", tool_context(request, "IP Lookup", "ip_lookup"))


@app.get("/asn-lookup")
async def page_asn_lookup(request: Request):
    return templates.TemplateResponse("tools/asn_lookup.html", tool_context(request, "ASN Lookup", "asn_lookup"))


@app.get("/blacklist-checker")
async def page_blacklist_checker(request: Request):
    return templates.TemplateResponse("tools/blacklist_checker.html", tool_context(request, "Blacklist Checker", "blacklist_checker"))


@app.get("/my-ip")
async def page_my_ip(request: Request):
    return templates.TemplateResponse("tools/my_ip.html", tool_context(request, "My IP Address", "my_ip"))


@app.get("/ua-checker")
async def page_ua_checker(request: Request):
    return templates.TemplateResponse("tools/ua_checker.html", tool_context(request, "User-Agent Checker", "ua_checker"))


@app.get("/email-validator")
async def page_email_validator(request: Request):
    return templates.TemplateResponse("tools/email_validator.html", tool_context(request, "Email Validator", "email_validator"))


@app.get("/ns-lookup")
async def page_ns_lookup(request: Request):
    return templates.TemplateResponse("tools/ns_lookup.html", tool_context(request, "NS Lookup", "ns_lookup"))


@app.get("/port-scanner")
async def page_port_scanner(request: Request):
    return templates.TemplateResponse("tools/port_scanner.html", tool_context(request, "Port Scanner", "port_scanner"))


@app.get("/cdn-detect")
async def page_cdn_detect(request: Request):
    return templates.TemplateResponse("tools/cdn_detect.html", tool_context(request, "CDN Detection", "cdn_detect"))


@app.get("/batch-lookup")
async def page_batch_lookup(request: Request):
    return templates.TemplateResponse("tools/batch_lookup.html", tool_context(request, "Batch Lookup", "batch_lookup"))


@app.get("/compare")
async def page_compare(request: Request):
    return templates.TemplateResponse("tools/compare.html", tool_context(request, "Tool Comparison", "compare"))


@app.get("/traceroute")
async def page_traceroute(request: Request):
    return templates.TemplateResponse("tools/traceroute.html", tool_context(request, "Traceroute", "traceroute"))


@app.get("/tech-detector")
async def page_tech_detector(request: Request):
    return templates.TemplateResponse("tools/tech_detector.html", tool_context(request, "Technology Detector", "tech_detector"))


@app.get("/speed-test")
async def page_speed_test(request: Request):
    return templates.TemplateResponse("tools/speed_test.html", tool_context(request, "Website Speed Test", "speed_test"))


@app.get("/dns-history")
async def page_dns_history(request: Request):
    return templates.TemplateResponse("tools/dns_history.html", tool_context(request, "DNS History", "dns_history"))


@app.get("/ssl-history")
async def page_ssl_history(request: Request):
    return templates.TemplateResponse("tools/ssl_history.html", tool_context(request, "SSL History", "ssl_history"))


@app.get("/api-dashboard")
async def page_api_dashboard(request: Request):
    return templates.TemplateResponse("tools/api_dashboard.html", tool_context(request, "API Dashboard", "api_dashboard"))


# ============ Dashboard Pages (Fase 2) ============

from fastapi.responses import RedirectResponse


@app.get("/dashboard")
async def page_dashboard(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "title": "Dashboard", "meta": None})


@app.get("/dashboard/domains")
async def page_domains(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/domains.html", {"request": request, "user": user, "title": "Domain Saya", "meta": None})


@app.get("/dashboard/domains/{domain_id}")
async def page_domain_detail(request: Request, domain_id: int):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/domain_detail.html", {"request": request, "user": user, "domain_id": domain_id, "title": "Detail Domain", "meta": None})


@app.get("/dashboard/api-keys")
async def page_api_keys(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/api_keys.html", {"request": request, "user": user, "title": "API Keys", "meta": None})


@app.get("/dashboard/notifications")
async def page_notifications(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/notifications.html", {"request": request, "user": user, "title": "Notifikasi", "meta": None})


@app.get("/dashboard/profile")
async def page_profile(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/profile.html", {"request": request, "user": user, "title": "Profil", "meta": None})


@app.get("/dashboard/ddns")
async def page_ddns(request: Request):
    from app.dependencies import get_current_user_optional
    user = await get_current_user_optional(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard/ddns.html", {"request": request, "user": user, "title": "Dynamic DNS", "meta": None})


@app.get("/login")
async def page_login(request: Request):
    return templates.TemplateResponse("dashboard/login.html", {"request": request, "title": "Login", "meta": None})


@app.get("/register")
async def page_register(request: Request):
    return templates.TemplateResponse("dashboard/register.html", {"request": request, "title": "Register", "meta": None})


# Health check (API)
@app.get("/health")
async def health():
    import sys
    from app.utils.cache import get_cache_stats
    uptime_seconds = int(time.time() - _server_start_time)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    uptime_str = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": "Memahami. Mengelola. Mengembangkan Internet.",
        "python": sys.version.split()[0],
        "uptime": uptime_str,
        "cache": get_cache_stats(),
        "rate_limit": f"{settings.RATE_LIMIT_PER_MINUTE} req/min",
    }


# robots.txt
@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    content = """User-agent: *
Allow: /
Disallow: /api/
Disallow: /docs
Disallow: /redoc
Disallow: /openapi.json

Sitemap: https://konektivitas.com/sitemap.xml"""
    return Response(content=content, media_type="text/plain")


# Dynamic sitemap.xml
@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap_xml():
    pages = [
        ("/", "1.0", "weekly"),
        ("/dns-lookup", "0.9", "monthly"),
        ("/dns-propagation", "0.9", "monthly"),
        ("/reverse-dns", "0.8", "monthly"),
        ("/mx-lookup", "0.8", "monthly"),
        ("/txt-lookup", "0.8", "monthly"),
        ("/cname-lookup", "0.7", "monthly"),
        ("/spf-checker", "0.8", "monthly"),
        ("/dmarc-checker", "0.8", "monthly"),
        ("/ns-lookup", "0.8", "monthly"),
        ("/whois-lookup", "0.9", "monthly"),
        ("/domain-expiry", "0.8", "monthly"),
        ("/ssl-checker", "0.9", "monthly"),
        ("/ssl-expiry", "0.8", "monthly"),
        ("/ping-checker", "0.9", "monthly"),
        ("/http-status", "0.8", "monthly"),
        ("/redirect-checker", "0.8", "monthly"),
        ("/header-checker", "0.7", "monthly"),
        ("/ua-checker", "0.8", "monthly"),
        ("/ip-lookup", "0.9", "monthly"),
        ("/my-ip", "0.9", "monthly"),
        ("/asn-lookup", "0.8", "monthly"),
        ("/blacklist-checker", "0.8", "monthly"),
        ("/email-validator", "0.8", "monthly"),
        ("/port-scanner", "0.8", "monthly"),
        ("/cdn-detect", "0.8", "monthly"),
        ("/batch-lookup", "0.8", "monthly"),
        ("/compare", "0.8", "monthly"),
        ("/traceroute", "0.8", "monthly"),
        ("/tech-detector", "0.8", "monthly"),
        ("/speed-test", "0.8", "monthly"),
        ("/dns-history", "0.8", "monthly"),
        ("/ssl-history", "0.8", "monthly"),
        ("/api-dashboard", "0.7", "monthly"),
        ("/about", "0.7", "monthly"),
        ("/api-docs", "0.7", "monthly"),
    ]
    
    urls_xml = "\n".join([
        f"""  <url>
    <loc>https://konektivitas.com{path}</loc>
    <lastmod>{date.today().isoformat()}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        for path, priority, freq in pages
    ])
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>"""
    return Response(content=sitemap, media_type="application/xml")


# 404 Handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"error": "Endpoint tidak ditemukan"})
    return template_response("404.html", request, title="404 - Tidak Ditemukan", meta=None, status_code=404)