"""Router untuk tool tambahan Fase 2: Traceroute, Tech Detector, Speed Test, DNS History, SSL History, API Dashboard"""
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from app.services import traceroute_service, tech_detector_service, speed_test_service
from app.services import dns_history_service, ssl_history_service
from app.services import api_dashboard_service
from app.utils.validators import validate_host, validate_url, sanitize_input
from app.utils.rate_limit import get_client_ip

router = APIRouter()


# ============ TRACEROUTE ============

@router.get("/traceroute/{host}")
async def traceroute_check(host: str):
    """Traceroute - Trace route ke server tujuan"""
    host = sanitize_input(host)
    valid, error = validate_host(host)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await traceroute_service.traceroute(host)


# ============ TECHNOLOGY DETECTOR ============

@router.get("/tech/{domain}/detect")
async def tech_detect(domain: str):
    """Technology Detector - Deteksi teknologi website"""
    domain = sanitize_input(domain)
    url = domain if domain.startswith(('http://', 'https://')) else f'https://{domain}'
    valid, error = validate_url(url)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await tech_detector_service.detect_technologies(url)


# ============ SPEED TEST ============

@router.get("/speed/{domain}")
async def speed_test(domain: str):
    """Speed Test - Test kecepatan loading website"""
    domain = sanitize_input(domain)
    url = domain if domain.startswith(('http://', 'https://')) else f'https://{domain}'
    valid, error = validate_url(url)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await speed_test_service.test_speed(url)


# ============ DNS HISTORY ============

@router.get("/dns/{domain}/history")
async def dns_history(
    domain: str,
    record_type: str = Query("A", description="Jenis DNS record"),
):
    """DNS History - Riwayat DNS record dari multiple nameserver"""
    domain = sanitize_input(domain)
    valid, error = validate_host(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})

    valid_types = ["A", "AAAA", "MX", "TXT", "CNAME", "NS", "SOA", "SRV", "CAA"]
    record_type = record_type.upper()
    if record_type not in valid_types:
        return JSONResponse(
            status_code=400,
            content={"error": f"record_type harus salah satu dari: {', '.join(valid_types)}"},
        )

    return await dns_history_service.get_dns_history(domain, record_type)


@router.get("/dns/{domain}/all-records")
async def dns_all_records(domain: str):
    """DNS History - Semua jenis record untuk domain"""
    domain = sanitize_input(domain)
    valid, error = validate_host(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await dns_history_service.get_all_record_types(domain)


# ============ SSL HISTORY ============

@router.get("/ssl/{domain}/cert-history")
async def ssl_cert_history(domain: str):
    """SSL History - Riwayat SSL certificate dari Certificate Transparency logs"""
    domain = sanitize_input(domain)
    valid, error = validate_host(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await ssl_history_service.get_ssl_history(domain)


# ============ API DASHBOARD ============

@router.get("/dashboard/stats")
async def api_dashboard_stats(request: Request):
    """API Dashboard - Statistik usage dan rate limit info"""
    ip = get_client_ip(request)
    return api_dashboard_service.get_api_dashboard(ip)
