from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services import cdn_service
from app.utils.validators import validate_domain, sanitize_input

router = APIRouter()


@router.get("/cdn/{domain}/detect")
async def cdn_detect(domain: str):
    """CDN Detection - Deteksi provider CDN untuk domain"""
    domain = sanitize_input(domain)
    valid, error = validate_domain(domain)
    if not valid:
        return JSONResponse(status_code=400, content={"error": error})
    return await cdn_service.detect_cdn(domain)
