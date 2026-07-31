from fastapi import APIRouter
from app.services import whois_service

router = APIRouter()


@router.get("/whois/{domain}")
async def whois_lookup(domain: str):
    """WHOIS Lookup - Informasi registrasi domain"""
    return await whois_service.lookup_whois(domain)


@router.get("/domain/{domain}/expiry")
async def domain_expiry(domain: str):
    """Domain Expiry Checker - Cek masa aktif domain"""
    return await whois_service.check_domain_expiry(domain)