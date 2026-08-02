from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services import dns_service
from app.utils.validators import validate_domain, validate_ip, sanitize_input

router = APIRouter()


@router.get("/dns/{domain}")
async def dns_lookup(domain: str, record_type: str = Query("A", description="Record type: A, AAAA, MX, TXT, CNAME, NS")):
    """DNS Lookup - Query DNS records untuk domain"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.lookup_dns(domain, record_type)


@router.get("/dns/{domain}/reverse")
async def reverse_dns(domain: str):
    """Reverse DNS - Lookup IP ke domain (menerima IP address)"""
    domain = sanitize_input(domain)
    valid, error = validate_ip(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.reverse_dns(domain)


@router.get("/dns/{domain}/mx")
async def mx_lookup(domain: str):
    """MX Lookup - Cek mail exchange records"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.lookup_mx(domain)


@router.get("/dns/{domain}/txt")
async def txt_lookup(domain: str):
    """TXT Lookup - Cek TXT records"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.lookup_txt(domain)


@router.get("/dns/{domain}/cname")
async def cname_lookup(domain: str):
    """CNAME Lookup - Cek canonical name records"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.lookup_cname(domain)


@router.get("/dns/{domain}/spf")
async def spf_checker(domain: str):
    """SPF Checker - Validasi SPF records"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.check_spf(domain)


@router.get("/dns/{domain}/dmarc")
async def dmarc_checker(domain: str):
    """DMARC Checker - Validasi DMARC policies"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.check_dmarc(domain)


@router.get("/dns/{domain}/propagation")
async def dns_propagation(domain: str, record_type: str = Query("A", description="Record type: A, AAAA, MX, TXT, CNAME, NS")):
    """DNS Propagation Checker - Cek DNS dari multiple nameserver global"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_service.propagation_check(domain, record_type)
