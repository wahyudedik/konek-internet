"""
API Key service — create, list, revoke, validate API keys.
"""

from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.api_key import ApiKey
from app.models.user import User
from app.utils.security import generate_api_key, verify_api_key


class ApiKeyService:
    """Service for API key management."""

    @staticmethod
    async def create_key(
        db: AsyncSession,
        user: User,
        name: str,
        permissions: str = "read",
        rate_limit: int = 120,
        expires_days: Optional[int] = None,
    ) -> dict:
        """
        Create a new API key for a user.
        
        Returns:
            dict with full_key (shown ONCE), key info
        """
        # Check limit — max 10 active keys per user
        result = await db.execute(
            select(ApiKey).where(
                ApiKey.user_id == user.id,
                ApiKey.is_active == True,
            )
        )
        active_keys = result.scalars().all()
        if len(active_keys) >= 10:
            raise ValueError("Maksimal 10 API key aktif. Cabut key yang tidak dipakai.")

        # Generate key
        full_key, key_hash, key_prefix = generate_api_key()

        # Calculate expiration
        expires_at = None
        if expires_days:
            from datetime import timedelta
            expires_at = datetime.utcnow() + timedelta(days=expires_days)

        # Create key record
        api_key = ApiKey(
            user_id=user.id,
            key_prefix=key_prefix,
            key_hash=key_hash,
            name=name,
            permissions=permissions,
            rate_limit=rate_limit,
            is_active=True,
            expires_at=expires_at,
        )
        db.add(api_key)
        await db.flush()

        return {
            "id": api_key.id,
            "key": full_key,  # Show ONCE — user must save this
            "key_prefix": api_key.key_prefix,
            "name": api_key.name,
            "permissions": api_key.permissions,
            "rate_limit": api_key.rate_limit,
            "is_active": api_key.is_active,
            "created_at": api_key.created_at.isoformat() if api_key.created_at else None,
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
            "warning": "Simpan API key ini baik-baik. Key hanya ditampilkan sekali.",
        }

    @staticmethod
    async def list_keys(db: AsyncSession, user: User) -> List[dict]:
        """List all API keys for a user (without exposing full key)."""
        result = await db.execute(
            select(ApiKey).where(ApiKey.user_id == user.id).order_by(ApiKey.created_at.desc())
        )
        keys = result.scalars().all()

        return [
            {
                "id": key.id,
                "key_prefix": key.key_prefix + "..." + "*" * 20,
                "name": key.name,
                "permissions": key.permissions,
                "rate_limit": key.rate_limit,
                "is_active": key.is_active,
                "created_at": key.created_at.isoformat() if key.created_at else None,
                "last_used_at": key.last_used_at.isoformat() if key.last_used_at else None,
                "expires_at": key.expires_at.isoformat() if key.expires_at else None,
            }
            for key in keys
        ]

    @staticmethod
    async def revoke_key(db: AsyncSession, user: User, key_id: int) -> bool:
        """
        Revoke (deactivate) an API key.
        Returns True if successful, False if key not found or not owned by user.
        """
        result = await db.execute(
            select(ApiKey).where(
                ApiKey.id == key_id,
                ApiKey.user_id == user.id,
            )
        )
        api_key = result.scalar_one_or_none()

        if api_key is None:
            return False

        api_key.is_active = False
        api_key.updated_at = datetime.utcnow()
        await db.flush()
        return True

    @staticmethod
    async def get_key_usage(db: AsyncSession, user: User, key_id: int) -> Optional[dict]:
        """Get usage stats for an API key."""
        result = await db.execute(
            select(ApiKey).where(
                ApiKey.id == key_id,
                ApiKey.user_id == user.id,
            )
        )
        api_key = result.scalar_one_or_none()

        if api_key is None:
            return None

        return {
            "id": api_key.id,
            "key_prefix": api_key.key_prefix,
            "name": api_key.name,
            "permissions": api_key.permissions,
            "rate_limit": api_key.rate_limit,
            "is_active": api_key.is_active,
            "created_at": api_key.created_at.isoformat() if api_key.created_at else None,
            "last_used_at": api_key.last_used_at.isoformat() if api_key.last_used_at else None,
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
        }
