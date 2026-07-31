from fastapi import APIRouter
from app.services import ssl_service

router = APIRouter()


@router.get("/ssl/{domain}")
async def ssl_checker(domain: str):
    """SSL Checker - Verifikasi sertifikat SSL"""
    return await ssl_service.check_ssl(domain)


@router.get("/ssl/{domain}/expiry")
async def ssl_expiry(domain: str):
    """SSL Expiry Checker - Cek masa aktif SSL"""
    return await ssl_service.check_ssl_expiry(domain)