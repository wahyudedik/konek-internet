from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.services import dns_service, ssl_service, whois_service
from app.utils.validators import validate_domain, sanitize_input
import asyncio

router = APIRouter()


@router.post("/compare")
async def compare_domains(
    domain1: str = Body(..., embed=True, description="First domain"),
    domain2: str = Body(..., embed=True, description="Second domain"),
    check_type: str = Body("dns", embed=True, description="Check type: dns, ssl, whois")
):
    """Compare - Bandingkan 2 domain side-by-side (DNS, SSL, atau WHOIS)"""
    domain1 = sanitize_input(domain1.strip().lower())
    domain2 = sanitize_input(domain2.strip().lower())

    if not domain1 or not domain2:
        return JSONResponse(status_code=400, content={"error": "Kedua domain harus diisi"})

    valid1, err1 = validate_domain(domain1)
    if not valid1:
        return JSONResponse(status_code=400, content={"error": f"Domain 1 '{domain1}' tidak valid: {err1}"})

    valid2, err2 = validate_domain(domain2)
    if not valid2:
        return JSONResponse(status_code=400, content={"error": f"Domain 2 '{domain2}' tidak valid: {err2}"})

    if check_type not in ("dns", "ssl", "whois"):
        return JSONResponse(status_code=400, content={"error": "check_type harus 'dns', 'ssl', atau 'whois'"})

    async def fetch_data(domain: str) -> dict:
        try:
            if check_type == "dns":
                return await dns_service.lookup_dns(domain)
            elif check_type == "ssl":
                return await ssl_service.check_ssl(domain)
            else:
                return await whois_service.lookup_whois(domain)
        except Exception as e:
            return {"error": str(e)}

    # Fetch both in parallel
    data1, data2 = await asyncio.gather(
        fetch_data(domain1),
        fetch_data(domain2)
    )

    return {
        "check_type": check_type,
        "domain1": domain1,
        "domain2": domain2,
        "data1": data1,
        "data2": data2
    }
