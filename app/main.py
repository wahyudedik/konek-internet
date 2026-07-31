import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.routers import dns, domain, ssl, website, ip
from app.utils.rate_limit import check_rate_limit, get_client_ip, get_remaining_requests

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ============ MIDDLEWARE ============

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = round((time.time() - start_time) * 1000, 2)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Performance header
        response.headers["X-Process-Time"] = f"{process_time}ms"
        
        # HSTS for production (only when HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


app.add_middleware(SecurityHeadersMiddleware)


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
                    content={"error": "Rate limit exceeded. Coba lagi dalam 1 menit.", "retry_after": 60}
                )
        
        response = await call_next(request)
        
        # Add rate limit headers for API
        if path.startswith("/api/"):
            ip = get_client_ip(request)
            remaining = get_remaining_requests(ip)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Limit"] = "60"
        
        return response


app.add_middleware(RateLimitMiddleware)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# API routers
app.include_router(dns.router, prefix="/api/v1", tags=["DNS"])
app.include_router(domain.router, prefix="/api/v1", tags=["Domain"])
app.include_router(ssl.router, prefix="/api/v1", tags=["SSL"])
app.include_router(website.router, prefix="/api/v1", tags=["Website"])
app.include_router(ip.router, prefix="/api/v1", tags=["IP"])


# ============ PAGE ROUTES ============

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Beranda"})


@app.get("/dns-lookup")
async def page_dns_lookup(request: Request):
    return templates.TemplateResponse("tools/dns_lookup.html", {"request": request, "title": "DNS Lookup"})


@app.get("/reverse-dns")
async def page_reverse_dns(request: Request):
    return templates.TemplateResponse("tools/reverse_dns.html", {"request": request, "title": "Reverse DNS"})


@app.get("/dns-propagation")
async def page_dns_propagation(request: Request):
    return templates.TemplateResponse("tools/dns_propagation.html", {"request": request, "title": "DNS Propagation Checker"})


@app.get("/mx-lookup")
async def page_mx_lookup(request: Request):
    return templates.TemplateResponse("tools/mx_lookup.html", {"request": request, "title": "MX Lookup"})


@app.get("/txt-lookup")
async def page_txt_lookup(request: Request):
    return templates.TemplateResponse("tools/txt_lookup.html", {"request": request, "title": "TXT Lookup"})


@app.get("/cname-lookup")
async def page_cname_lookup(request: Request):
    return templates.TemplateResponse("tools/cname_lookup.html", {"request": request, "title": "CNAME Lookup"})


@app.get("/spf-checker")
async def page_spf_checker(request: Request):
    return templates.TemplateResponse("tools/spf_checker.html", {"request": request, "title": "SPF Checker"})


@app.get("/dmarc-checker")
async def page_dmarc_checker(request: Request):
    return templates.TemplateResponse("tools/dmarc_checker.html", {"request": request, "title": "DMARC Checker"})


@app.get("/whois-lookup")
async def page_whois_lookup(request: Request):
    return templates.TemplateResponse("tools/whois_lookup.html", {"request": request, "title": "WHOIS Lookup"})


@app.get("/domain-expiry")
async def page_domain_expiry(request: Request):
    return templates.TemplateResponse("tools/domain_expiry.html", {"request": request, "title": "Domain Expiry Checker"})


@app.get("/ssl-checker")
async def page_ssl_checker(request: Request):
    return templates.TemplateResponse("tools/ssl_checker.html", {"request": request, "title": "SSL Checker"})


@app.get("/ssl-expiry")
async def page_ssl_expiry(request: Request):
    return templates.TemplateResponse("tools/ssl_expiry.html", {"request": request, "title": "SSL Expiry Checker"})


@app.get("/ping-checker")
async def page_ping_checker(request: Request):
    return templates.TemplateResponse("tools/ping_checker.html", {"request": request, "title": "Ping Checker"})


@app.get("/http-status")
async def page_http_status(request: Request):
    return templates.TemplateResponse("tools/http_status.html", {"request": request, "title": "HTTP Status Checker"})


@app.get("/redirect-checker")
async def page_redirect_checker(request: Request):
    return templates.TemplateResponse("tools/redirect_checker.html", {"request": request, "title": "Redirect Checker"})


@app.get("/header-checker")
async def page_header_checker(request: Request):
    return templates.TemplateResponse("tools/header_checker.html", {"request": request, "title": "Header Checker"})


@app.get("/ip-lookup")
async def page_ip_lookup(request: Request):
    return templates.TemplateResponse("tools/ip_lookup.html", {"request": request, "title": "IP Lookup"})


@app.get("/asn-lookup")
async def page_asn_lookup(request: Request):
    return templates.TemplateResponse("tools/asn_lookup.html", {"request": request, "title": "ASN Lookup"})


@app.get("/blacklist-checker")
async def page_blacklist_checker(request: Request):
    return templates.TemplateResponse("tools/blacklist_checker.html", {"request": request, "title": "Blacklist Checker"})


# Health check (API)
@app.get("/health")
async def health():
    import sys
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "python": sys.version.split()[0],
        "cache": "in-memory"
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
        ("/whois-lookup", "0.9", "monthly"),
        ("/domain-expiry", "0.8", "monthly"),
        ("/ssl-checker", "0.9", "monthly"),
        ("/ssl-expiry", "0.8", "monthly"),
        ("/ping-checker", "0.9", "monthly"),
        ("/http-status", "0.8", "monthly"),
        ("/redirect-checker", "0.8", "monthly"),
        ("/header-checker", "0.7", "monthly"),
        ("/ip-lookup", "0.9", "monthly"),
        ("/asn-lookup", "0.8", "monthly"),
        ("/blacklist-checker", "0.8", "monthly"),
    ]
    
    urls_xml = "\n".join([
        f"""  <url>
    <loc>https://konektivitas.com{path}</loc>
    <lastmod>2026-07-31</lastmod>
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
    return templates.TemplateResponse("404.html", {"request": request, "title": "404 - Tidak Ditemukan"}, status_code=404)