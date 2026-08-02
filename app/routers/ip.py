from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from app.services import ip_service
from app.services import email_service
from app.services import port_service
from app.utils.validators import validate_ip, validate_host, sanitize_input

router = APIRouter()


@router.get("/ip/me")
async def my_ip(request: Request):
    """My IP - Deteksi IP address Anda"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.headers.get("X-Real-IP", request.client.host if request.client else "unknown")
    result = await ip_service.lookup_ip(ip)
    result["is_your_ip"] = True
    return result


@router.get("/email/{email}/validate")
async def validate_email(email: str):
    """Email Validator - Validasi email address"""
    email = sanitize_input(email, max_length=254)
    valid, error = email_service.validate_email_format(email)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await email_service.validate_email(email)


@router.get("/port/{host}")
async def port_scan(host: str, ports: str = Query("80,443,22")):
    """Port Scanner - Scan port TCP"""
    host = sanitize_input(host)
    valid, error = validate_host(host)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    # Parse ports
    try:
        port_list = [int(p.strip()) for p in ports.split(",")]
        port_list = [p for p in port_list if 1 <= p <= 65535][:20]  # Max 20 ports
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Format port tidak valid"})
    if not port_list:
        return JSONResponse(status_code=400, content={"error": "Minimal 1 port harus ditentukan"})
    return await port_service.scan_ports(host, port_list)


@router.get("/ip/{ip_address}")
async def ip_lookup(ip_address: str):
    """IP Lookup - Informasi IP address"""
    ip_address = sanitize_input(ip_address)
    valid, error = validate_ip(ip_address)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ip_service.lookup_ip(ip_address)


@router.get("/ip/{ip_address}/asn")
async def asn_lookup(ip_address: str):
    """ASN Lookup - Cek Autonomous System Number"""
    ip_address = sanitize_input(ip_address)
    valid, error = validate_ip(ip_address)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ip_service.lookup_asn(ip_address)


@router.get("/ip/{ip_address}/blacklist")
async def blacklist_checker(ip_address: str):
    """Blacklist Checker - Cek apakah IP ada di blacklist"""
    ip_address = sanitize_input(ip_address)
    valid, error = validate_ip(ip_address)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ip_service.check_blacklist(ip_address)
