from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.services import dns_service, ssl_service, whois_service
from app.utils.validators import validate_domain, sanitize_input
import asyncio

router = APIRouter()

MAX_BATCH_SIZE = 10


@router.post("/batch")
async def batch_lookup(
    domains: list[str] = Body(..., embed=True, description="List of domains (max 10)"),
    check_type: str = Body("dns", embed=True, description="Check type: dns, ssl, whois")
):
    """Batch Lookup - Cek multiple domain sekaligus (DNS, SSL, atau WHOIS)"""
    if not domains:
        return JSONResponse(status_code=400, content={"error": "Domain list tidak boleh kosong"})
    
    if len(domains) > MAX_BATCH_SIZE:
        return JSONResponse(
            status_code=400,
            content={"error": f"Maksimal {MAX_BATCH_SIZE} domain per batch"}
        )
    
    if check_type not in ("dns", "ssl", "whois"):
        return JSONResponse(
            status_code=400,
            content={"error": "check_type harus 'dns', 'ssl', atau 'whois'"}
        )
    
    # Validate and sanitize all domains first
    clean_domains = []
    for d in domains:
        d = sanitize_input(d.strip().lower())
        if not d:
            continue
        valid, error = validate_domain(d)
        if not valid:
            return JSONResponse(
                status_code=400,
                content={"error": f"Domain '{d}' tidak valid: {error}"}
            )
        clean_domains.append(d)
    
    if not clean_domains:
        return JSONResponse(status_code=400, content={"error": "Tidak ada domain valid untuk dicek"})
    
    # Process all domains in parallel
    async def check_domain(domain: str) -> dict:
        try:
            if check_type == "dns":
                result = await dns_service.lookup_dns(domain)
            elif check_type == "ssl":
                result = await ssl_service.check_ssl(domain)
            else:
                result = await whois_service.lookup_whois(domain)
            return {"domain": domain, "status": "ok", "data": result}
        except Exception as e:
            return {"domain": domain, "status": "error", "error": str(e)}
    
    results = await asyncio.gather(*[check_domain(d) for d in clean_domains])
    
    return {
        "check_type": check_type,
        "total": len(results),
        "results": list(results)
    }
