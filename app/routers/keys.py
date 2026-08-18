"""
API Key management endpoints — create, list, revoke, usage.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.api_key_service import ApiKeyService

router = APIRouter(prefix="/keys", tags=["API Keys"])


# ============ Request/Response Models ============

class CreateKeyRequest(BaseModel):
    name: str
    permissions: str = "read"  # read, write, admin
    rate_limit: int = 120
    expires_days: Optional[int] = None


class CreateKeyResponse(BaseModel):
    id: int
    key: str
    key_prefix: str
    name: str
    permissions: str
    rate_limit: int
    is_active: bool
    created_at: Optional[str]
    expires_at: Optional[str]
    warning: str


class KeyInfo(BaseModel):
    id: int
    key_prefix: str
    name: str
    permissions: str
    rate_limit: int
    is_active: bool
    created_at: Optional[str]
    last_used_at: Optional[str]
    expires_at: Optional[str]


class MessageResponse(BaseModel):
    message: str


# ============ Endpoints ============

@router.get("", response_model=list[KeyInfo])
async def list_api_keys(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all API keys for the current user."""
    keys = await ApiKeyService.list_keys(db=db, user=user)
    return keys


@router.post("", response_model=CreateKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateKeyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new API key. Save the key — it's only shown once!"""
    try:
        key_data = await ApiKeyService.create_key(
            db=db,
            user=user,
            name=request.name,
            permissions=request.permissions,
            rate_limit=request.rate_limit,
            expires_days=request.expires_days,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return key_data


@router.delete("/{key_id}", response_model=MessageResponse)
async def revoke_api_key(
    key_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Revoke (deactivate) an API key."""
    success = await ApiKeyService.revoke_key(db=db, user=user, key_id=key_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key tidak ditemukan.",
        )

    return MessageResponse(message="API key berhasil dicabut.")


@router.get("/{key_id}/usage", response_model=KeyInfo)
async def get_key_usage(
    key_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get usage stats for an API key."""
    usage = await ApiKeyService.get_key_usage(db=db, user=user, key_id=key_id)

    if usage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key tidak ditemukan.",
        )

    return usage
