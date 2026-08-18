"""
Dynamic DNS service — Kelola DNS record update via API.

Fitur:
- Buat, baca, update, hapus DDNS records
- Update IP via token (tanpa auth - untuk client devices)
- Validasi token dan rate limit per update
- Integrasi Cloudflare (manual mode untuk MVP)
"""

import json
import logging
import secrets
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ddns import DynamicDns

logger = logging.getLogger("konektivitas.ddns")

# Rate limit: minimum 60 detik antar update per record
MIN_UPDATE_INTERVAL_SECONDS = 60


class DdnsService:
    """Service for Dynamic DNS CRUD operations."""

    @staticmethod
    def generate_token() -> str:
        """Generate a unique DDNS update token."""
        return secrets.token_urlsafe(32)

    @staticmethod
    async def create_record(
        db: AsyncSession,
        user_id: int,
        hostname: str,
        domain: str,
        record_type: str = "A",
        provider: str = "manual",
        provider_config: Optional[dict] = None,
        ttl: int = 300,
        update_interval_minutes: int = 5,
    ) -> dict:
        """
        Create a new DDNS record.
        
        Returns the record with the token (shown only once).
        """
        token = DdnsService.generate_token()
        
        record = DynamicDns(
            user_id=user_id,
            hostname=hostname,
            domain=domain,
            record_type=record_type.upper(),
            token=token,
            provider=provider,
            provider_config=json.dumps(provider_config) if provider_config else None,
            ttl=ttl,
            update_interval_minutes=update_interval_minutes,
            is_active=True,
        )
        
        db.add(record)
        await db.flush()
        await db.refresh(record)
        
        logger.info("DDNS record created: %s (user_id=%d)", hostname, user_id)
        
        return {
            "id": record.id,
            "hostname": record.hostname,
            "domain": record.domain,
            "record_type": record.record_type,
            "token": token,  # Shown ONCE
            "provider": record.provider,
            "current_ip": record.current_ip,
            "is_active": record.is_active,
            "update_interval_minutes": record.update_interval_minutes,
            "ttl": record.ttl,
            "last_updated": record.last_updated.isoformat() if record.last_updated else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        }

    @staticmethod
    async def list_records(
        db: AsyncSession,
        user_id: int,
    ) -> List[dict]:
        """List all DDNS records for a user."""
        result = await db.execute(
            select(DynamicDns)
            .where(DynamicDns.user_id == user_id)
            .order_by(DynamicDns.created_at.desc())
        )
        records = result.scalars().all()
        
        return [
            {
                "id": r.id,
                "hostname": r.hostname,
                "domain": r.domain,
                "record_type": r.record_type,
                "provider": r.provider,
                "current_ip": r.current_ip,
                "is_active": r.is_active,
                "update_interval_minutes": r.update_interval_minutes,
                "ttl": r.ttl,
                "last_updated": r.last_updated.isoformat() if r.last_updated else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]

    @staticmethod
    async def get_record(
        db: AsyncSession,
        user_id: int,
        record_id: int,
    ) -> Optional[dict]:
        """Get a single DDNS record by ID."""
        result = await db.execute(
            select(DynamicDns)
            .where(DynamicDns.id == record_id, DynamicDns.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return None
        
        return {
            "id": record.id,
            "hostname": record.hostname,
            "domain": record.domain,
            "record_type": record.record_type,
            "provider": record.provider,
            "provider_config": json.loads(record.provider_config) if record.provider_config else None,
            "current_ip": record.current_ip,
            "is_active": record.is_active,
            "update_interval_minutes": record.update_interval_minutes,
            "ttl": record.ttl,
            "last_updated": record.last_updated.isoformat() if record.last_updated else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        }

    @staticmethod
    async def update_record(
        db: AsyncSession,
        user_id: int,
        record_id: int,
        hostname: Optional[str] = None,
        record_type: Optional[str] = None,
        provider: Optional[str] = None,
        provider_config: Optional[dict] = None,
        is_active: Optional[bool] = None,
        update_interval_minutes: Optional[int] = None,
        ttl: Optional[int] = None,
    ) -> Optional[dict]:
        """Update a DDNS record's configuration."""
        result = await db.execute(
            select(DynamicDns)
            .where(DynamicDns.id == record_id, DynamicDns.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return None
        
        if hostname is not None:
            record.hostname = hostname
        if record_type is not None:
            record.record_type = record_type.upper()
        if provider is not None:
            record.provider = provider
        if provider_config is not None:
            record.provider_config = json.dumps(provider_config)
        if is_active is not None:
            record.is_active = is_active
        if update_interval_minutes is not None:
            record.update_interval_minutes = update_interval_minutes
        if ttl is not None:
            record.ttl = ttl
        
        await db.flush()
        await db.refresh(record)
        
        logger.info("DDNS record updated: id=%d (user_id=%d)", record_id, user_id)
        
        return {
            "id": record.id,
            "hostname": record.hostname,
            "domain": record.domain,
            "record_type": record.record_type,
            "provider": record.provider,
            "current_ip": record.current_ip,
            "is_active": record.is_active,
            "update_interval_minutes": record.update_interval_minutes,
            "ttl": record.ttl,
            "last_updated": record.last_updated.isoformat() if record.last_updated else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        }

    @staticmethod
    async def delete_record(
        db: AsyncSession,
        user_id: int,
        record_id: int,
    ) -> bool:
        """Delete a DDNS record."""
        result = await db.execute(
            select(DynamicDns)
            .where(DynamicDns.id == record_id, DynamicDns.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return False
        
        await db.delete(record)
        await db.flush()
        
        logger.info("DDNS record deleted: id=%d, hostname=%s (user_id=%d)", record_id, record.hostname, user_id)
        return True

    @staticmethod
    async def update_ip_by_token(
        db: AsyncSession,
        token: str,
        ip_address: str,
    ) -> Dict[str, Any]:
        """
        Update IP address for a DDNS record using token (no auth required).
        
        This is the main endpoint for client devices (routers, IoT, etc).
        Rate limited: minimum 60 seconds between updates per record.
        
        Returns status dict with success/error info.
        """
        result = await db.execute(
            select(DynamicDns).where(DynamicDns.token == token)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return {"success": False, "error": "Token tidak valid"}
        
        if not record.is_active:
            return {"success": False, "error": "Record tidak aktif", "hostname": record.hostname}
        
        # Rate limit check
        if record.last_updated:
            now = datetime.now(timezone.utc)
            last_update = record.last_updated
            if last_update.tzinfo is None:
                last_update = last_update.replace(tzinfo=timezone.utc)
            elapsed = (now - last_update).total_seconds()
            if elapsed < MIN_UPDATE_INTERVAL_SECONDS:
                remaining = int(MIN_UPDATE_INTERVAL_SECONDS - elapsed)
                return {
                    "success": False,
                    "error": f"Rate limit: tunggu {remaining} detik lagi",
                    "hostname": record.hostname,
                    "next_update_in_seconds": remaining,
                }
        
        # Check if IP actually changed
        ip_changed = record.current_ip != ip_address
        
        # Update
        record.current_ip = ip_address
        record.last_updated = datetime.now(timezone.utc)
        await db.flush()
        
        logger.info(
            "DDNS update: %s -> %s (changed=%s)",
            record.hostname, ip_address, ip_changed
        )
        
        return {
            "success": True,
            "hostname": record.hostname,
            "ip": ip_address,
            "ip_changed": ip_changed,
            "record_type": record.record_type,
            "ttl": record.ttl,
            "last_updated": record.last_updated.isoformat() if record.last_updated else None,
        }

    @staticmethod
    async def regenerate_token(
        db: AsyncSession,
        user_id: int,
        record_id: int,
    ) -> Optional[dict]:
        """Regenerate the update token for a DDNS record."""
        result = await db.execute(
            select(DynamicDns)
            .where(DynamicDns.id == record_id, DynamicDns.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        
        if not record:
            return None
        
        new_token = DdnsService.generate_token()
        record.token = new_token
        await db.flush()
        await db.refresh(record)
        
        logger.info("DDNS token regenerated: id=%d, hostname=%s (user_id=%d)", record_id, record.hostname, user_id)
        
        return {
            "id": record.id,
            "hostname": record.hostname,
            "token": new_token,
            "message": "Token baru. Simpan di tempat aman - tidak akan ditampilkan lagi.",
        }
