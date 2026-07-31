from fastapi import APIRouter, Query
from app.services import dns_service

router = APIRouter()


@router.get("/dns/{domain}")
async def dns_lookup(domain: str, record_type: str = Query("A", description="Record type: A, AAAA, MX, TXT, CNAME, NS")):
    """DNS Lookup - Query DNS records untuk domain"""
    return await dns_service.lookup_dns(domain, record_type)


@router.get("/dns/{domain}/reverse")
async def reverse_dns(domain: str):
    """Reverse DNS - Lookup IP ke domain"""
    return await dns_service.reverse_dns(domain)


@router.get("/dns/{domain}/mx")
async def mx_lookup(domain: str):
    """MX Lookup - Cek mail exchange records"""
    return await dns_service.lookup_mx(domain)


@router.get("/dns/{domain}/txt")
async def txt_lookup(domain: str):
    """TXT Lookup - Cek TXT records"""
    return await dns_service.lookup_txt(domain)


@router.get("/dns/{domain}/cname")
async def cname_lookup(domain: str):
    """CNAME Lookup - Cek canonical name records"""
    return await dns_service.lookup_cname(domain)


@router.get("/dns/{domain}/spf")
async def spf_checker(domain: str):
    """SPF Checker - Validasi SPF records"""
    return await dns_service.check_spf(domain)


@router.get("/dns/{domain}/dmarc")
async def dmarc_checker(domain: str):
    """DMARC Checker - Validasi DMARC policies"""
    return await dns_service.check_dmarc(domain)