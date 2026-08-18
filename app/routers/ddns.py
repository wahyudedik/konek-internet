"""
Dynamic DNS API endpoints — CRUD + update via token.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ddns_service import DdnsService

router = APIRouter(prefix="/ddns", tags=["Dynamic DNS"])


# ============ Request/Response Models ============

class CreateDdnsRequest(BaseModel):
    hostname: str
    domain: str
    record_type: str = "A"
    provider: str = "manual"
    provider_config: Optional[dict] = None
    ttl: int = 300
    update_interval_minutes: int = 5


class UpdateDdnsRequest(BaseModel):
    hostname: Optional[str] = None
    record_type: Optional[str] = None
    provider: Optional[str] = None
    provider_config: Optional[dict] = None
    is_active: Optional[bool] = None
    update_interval_minutes: Optional[int] = None
    ttl: Optional[int] = None


class DdnsRecord(BaseModel):
    id: int
    hostname: str
    domain: str
    record_type: str
    provider: str
    token: Optional[str] = None  # Only returned on create/regenerate
    current_ip: Optional[str]
    is_active: bool
    update_interval_minutes: int
    ttl: int
    last_updated: Optional[str]
    created_at: Optional[str]


class DdnsRecordDetail(DdnsRecord):
    provider_config: Optional[dict] = None
    updated_at: Optional[str] = None


class DdnsTokenResponse(BaseModel):
    id: int
    hostname: str
    token: str
    message: str


class MessageResponse(BaseModel):
    message: str


class UpdateIpResponse(BaseModel):
    success: bool
    hostname: Optional[str] = None
    ip: Optional[str] = None
    ip_changed: Optional[bool] = None
    record_type: Optional[str] = None
    ttl: Optional[int] = None
    error: Optional[str] = None
    next_update_in_seconds: Optional[int] = None
    last_updated: Optional[str] = None


# ============ Authenticated Endpoints (CRUD) ============

@router.get("/records", response_model=List[DdnsRecord])
async def list_ddns_records(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all DDNS records for the current user."""
    return await DdnsService.list_records(db=db, user_id=user.id)


@router.post("/records", response_model=DdnsRecord, status_code=status.HTTP_201_CREATED)
async def create_ddns_record(
    request: CreateDdnsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new DDNS record.
    
    The token is returned ONCE. Save it securely - it's used to update the IP.
    """
    # Validate record type
    if request.record_type.upper() not in ("A", "AAAA"):
        raise HTTPException(status_code=400, detail="record_type harus A atau AAAA")
    
    # Validate TTL
    if request.ttl < 60 or request.ttl > 86400:
        raise HTTPException(status_code=400, detail="TTL harus antara 60-86400 detik")
    
    result = await DdnsService.create_record(
        db=db,
        user_id=user.id,
        hostname=request.hostname,
        domain=request.domain,
        record_type=request.record_type,
        provider=request.provider,
        provider_config=request.provider_config,
        ttl=request.ttl,
        update_interval_minutes=request.update_interval_minutes,
    )
    
    # Token is included in response but not in subsequent GET requests
    return result


@router.get("/records/{record_id}", response_model=DdnsRecordDetail)
async def get_ddns_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single DDNS record by ID."""
    record = await DdnsService.get_record(db=db, user_id=user.id, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record tidak ditemukan")
    return record


@router.put("/records/{record_id}", response_model=DdnsRecordDetail)
async def update_ddns_record(
    record_id: int,
    request: UpdateDdnsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a DDNS record's configuration."""
    result = await DdnsService.update_record(
        db=db,
        user_id=user.id,
        record_id=record_id,
        hostname=request.hostname,
        record_type=request.record_type,
        provider=request.provider,
        provider_config=request.provider_config,
        is_active=request.is_active,
        update_interval_minutes=request.update_interval_minutes,
        ttl=request.ttl,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Record tidak ditemukan")
    return result


@router.delete("/records/{record_id}", response_model=MessageResponse)
async def delete_ddns_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a DDNS record."""
    success = await DdnsService.delete_record(db=db, user_id=user.id, record_id=record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record tidak ditemukan")
    return MessageResponse(message="Record berhasil dihapus")


@router.post("/records/{record_id}/regenerate-token", response_model=DdnsTokenResponse)
async def regenerate_ddns_token(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Regenerate the update token for a DDNS record.
    
    The old token will stop working immediately.
    The new token is returned ONCE.
    """
    result = await DdnsService.regenerate_token(db=db, user_id=user.id, record_id=record_id)
    if not result:
        raise HTTPException(status_code=404, detail="Record tidak ditemukan")
    return result


# ============ Public Endpoint (Token-based, no auth) ============

@router.get("/update", response_model=UpdateIpResponse)
async def update_ip(
    token: str = Query(..., description="DDNS update token"),
    ip: str = Query(..., description="IP address baru"),
    db: AsyncSession = Depends(get_db),
):
    """
    Update IP address via token — Endpoint utama untuk client devices.
    
    Contoh penggunaan:
    - Router: `GET /api/v1/ddns/update?token=xxx&ip=1.2.3.4`
    - Cron job: `curl "https://konektivitas.com/api/v1/ddns/update?token=xxx&ip=$(curl -s ifconfig.me)"`
    - IoT Device: Periodic GET request dengan IP terkini
    
    Rate limit: Minimum 60 detik antar update per record.
    """
    # Validate IP format (basic)
    if not ip or len(ip) > 45:
        return UpdateIpResponse(success=False, error="Format IP tidak valid")
    
    result = await DdnsService.update_ip_by_token(db=db, token=token, ip_address=ip)
    
    if not result.get("success"):
        return UpdateIpResponse(
            success=False,
            hostname=result.get("hostname"),
            error=result.get("error"),
            next_update_in_seconds=result.get("next_update_in_seconds"),
        )
    
    return UpdateIpResponse(
        success=True,
        hostname=result["hostname"],
        ip=result["ip"],
        ip_changed=result["ip_changed"],
        record_type=result["record_type"],
        ttl=result["ttl"],
        last_updated=result["last_updated"],
    )
