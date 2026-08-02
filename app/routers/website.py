from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from app.services import website_service, ua_service
from app.utils.validators import validate_host, validate_url, sanitize_input

router = APIRouter()


@router.get("/ua")
async def ua_detect(request: Request):
    """User-Agent Checker - Auto-detect dari request"""
    ua_string = request.headers.get("User-Agent", "Unknown")
    return await ua_service.parse_ua(ua_string)


@router.get("/ua/{encoded_ua:path}")
async def ua_parse(encoded_ua: str):
    """User-Agent Checker - Parse UA spesifik"""
    encoded_ua = sanitize_input(encoded_ua, max_length=1000)
    if not encoded_ua:
        return JSONResponse(status_code=400, content={"error": "User-Agent string tidak boleh kosong"})
    return await ua_service.parse_ua(encoded_ua)


@router.get("/ping/{domain}")
async def ping_checker(domain: str):
    """Ping Checker - Uji konektivitas ke server"""
    domain = sanitize_input(domain)
    valid, error = validate_host(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await website_service.ping_host(domain)


@router.get("/http-status/{domain}")
async def http_status(domain: str):
    """HTTP Status Checker - Cek status HTTP response"""
    domain = sanitize_input(domain)
    # Auto-prepend https:// jika tidak ada protocol untuk validasi URL
    url = domain if domain.startswith(('http://', 'https://')) else f'https://{domain}'
    valid, error = validate_url(url)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await website_service.check_http_status(url)


@router.get("/redirect/{domain}")
async def redirect_checker(domain: str):
    """Redirect Checker - Lacak redirect chains"""
    domain = sanitize_input(domain)
    url = domain if domain.startswith(('http://', 'https://')) else f'https://{domain}'
    valid, error = validate_url(url)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await website_service.check_redirects(url)


@router.get("/headers/{domain}")
async def header_checker(domain: str):
    """Header Checker - Analisis HTTP headers"""
    domain = sanitize_input(domain)
    url = domain if domain.startswith(('http://', 'https://')) else f'https://{domain}'
    valid, error = validate_url(url)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await website_service.check_headers(url)
