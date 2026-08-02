from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services import whois_service
from app.utils.validators import validate_domain, sanitize_input

router = APIRouter()


@router.get("/whois/{domain}")
async def whois_lookup(domain: str):
    """WHOIS Lookup - Informasi registrasi domain"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await whois_service.lookup_whois(domain)


@router.get("/domain/{domain}/expiry")
async def domain_expiry(domain: str):
    """Domain Expiry Checker - Cek masa aktif domain"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await whois_service.check_domain_expiry(domain)
