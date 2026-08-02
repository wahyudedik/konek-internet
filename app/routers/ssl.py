from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services import ssl_service
from app.utils.validators import validate_domain, sanitize_input

router = APIRouter()


@router.get("/ssl/{domain}")
async def ssl_checker(domain: str):
    """SSL Checker - Verifikasi sertifikat SSL"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ssl_service.check_ssl(domain)


@router.get("/ssl/{domain}/expiry")
async def ssl_expiry(domain: str):
    """SSL Expiry Checker - Cek masa aktif SSL"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ssl_service.check_ssl_expiry(domain)
