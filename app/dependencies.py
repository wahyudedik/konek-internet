"""
FastAPI dependencies — database session, current user, API key validation.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.utils.security import decode_token, verify_api_key
from app.models.user import User
from app.models.api_key import ApiKey


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract and validate JWT token from Authorization header.
    Returns the authenticated User.
    
    Supports:
    - Bearer token in Authorization header
    - API key in X-API-Key header (attaches user from key owner)
    """
    # Try API key first
    api_key_value = request.headers.get("X-API-Key")
    if api_key_value:
        return await _get_user_from_api_key(api_key_value, db)

    # Try JWT token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tidak terautentikasi. Silakan login atau gunakan API key.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ", 1)[1]
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kadaluarsa.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check token type (reject refresh tokens for access)
    if payload.get("type") == "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Gunakan access token, bukan refresh token.",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid.",
        )

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan atau tidak aktif.",
        )

    return user


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Optional authentication — returns User if authenticated, None otherwise.
    Used for endpoints that behave differently for authenticated users.
    """
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None


async def _get_user_from_api_key(api_key_value: str, db: AsyncSession) -> User:
    """Validate API key and return the owner User."""
    if not api_key_value.startswith("kn_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key harus dimulai dengan 'kn_'.",
        )

    # Extract prefix for lookup (first 12 chars)
    key_prefix = api_key_value[:12]

    result = await db.execute(
        select(ApiKey).where(
            ApiKey.key_prefix == key_prefix,
            ApiKey.is_active == True,
        )
    )
    api_key = result.scalar_one_or_none()

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key tidak valid atau sudah dicabut.",
        )

    # Check expiration
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key sudah kadaluarsa.",
        )

    # Verify full key hash
    if not verify_api_key(api_key_value, api_key.key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key tidak valid.",
        )

    # Update last_used_at
    api_key.last_used_at = datetime.utcnow()
    await db.flush()

    # Get owner user
    result = await db.execute(select(User).where(User.id == api_key.user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pemilik API key tidak aktif.",
        )

    return user


def require_plan(*allowed_plans):
    """
    Dependency factory that checks user's subscription plan.
    
    Usage:
        @router.get("/premium-feature")
        async def premium(user = Depends(require_plan("pro", "team", "enterprise"))):
            ...
    """
    async def _check_plan(user: User = Depends(get_current_user)) -> User:
        if user.plan not in allowed_plans:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Fitur ini memerlukan plan: {', '.join(allowed_plans)}. Plan Anda: {user.plan}",
            )
        return user
    return _check_plan


# Required for datetime import in _get_user_from_api_key
from datetime import datetime


async def get_current_user_optional(request: Request) -> Optional[User]:
    """
    Standalone function (no Depends) for use in page routes.
    Extracts user from Authorization header if present.
    Returns None if not authenticated.
    """
    from app.database import async_session_factory

    # Try API key first
    api_key_value = request.headers.get("X-API-Key")
    # Try JWT token
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]

    if not api_key_value and not token:
        return None

    async with async_session_factory() as db:
        try:
            if api_key_value:
                return await _get_user_from_api_key(api_key_value, db)
            if token:
                payload = decode_token(token)
                if payload is None:
                    return None
                if payload.get("type") == "refresh":
                    return None
                user_id = payload.get("sub")
                if user_id is None:
                    return None
                result = await db.execute(select(User).where(User.id == int(user_id)))
                user = result.scalar_one_or_none()
                if user and user.is_active:
                    return user
        except Exception:
            pass

    return None
