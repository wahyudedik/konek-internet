"""
Workspace service — domain management, monitoring data access.
"""

from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.models.user import User
from app.models.monitored_domain import MonitoredDomain
from app.models.ssl_history import DomainSslHistory
from app.models.dns_history import DomainDnsHistory
from app.models.uptime_check import UptimeCheck, UptimeLog


class WorkspaceService:
    """Service for workspace domain management."""

    # ============ Domain Management ============

    @staticmethod
    async def add_domain(
        db: AsyncSession,
        user: User,
        domain: str,
        notes: Optional[str] = None,
        monitor_ssl: bool = True,
        monitor_dns: bool = True,
        monitor_uptime: bool = True,
    ) -> MonitoredDomain:
        """Add a domain to user's workspace."""
        # Check if domain already exists for this user
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.user_id == user.id,
                MonitoredDomain.domain == domain.lower(),
            )
        )
        if result.scalar_one_or_none():
            raise ValueError(f"Domain '{domain}' sudah ada di workspace.")

        # Normalize domain
        clean_domain = domain.lower().strip()
        if clean_domain.startswith("http://"):
            clean_domain = clean_domain[7:]
        if clean_domain.startswith("https://"):
            clean_domain = clean_domain[8:]
        clean_domain = clean_domain.rstrip("/")

        mon_domain = MonitoredDomain(
            user_id=user.id,
            domain=clean_domain,
            notes=notes,
            monitor_ssl=monitor_ssl,
            monitor_dns=monitor_dns,
            monitor_uptime=monitor_uptime,
        )
        db.add(mon_domain)
        await db.flush()

        # Create uptime check if monitoring is enabled
        if monitor_uptime:
            uptime_check = UptimeCheck(
                domain_id=mon_domain.id,
                url=f"https://{clean_domain}",
                method="GET",
                expected_status=200,
                timeout_seconds=10,
                is_active=True,
            )
            db.add(uptime_check)
            await db.flush()

        return mon_domain

    @staticmethod
    async def list_domains(db: AsyncSession, user: User) -> List[dict]:
        """List all domains in user's workspace."""
        result = await db.execute(
            select(MonitoredDomain)
            .where(MonitoredDomain.user_id == user.id)
            .order_by(desc(MonitoredDomain.created_at))
        )
        domains = result.scalars().all()

        return [
            {
                "id": d.id,
                "domain": d.domain,
                "notes": d.notes,
                "status": d.status,
                "monitor_ssl": d.monitor_ssl,
                "monitor_dns": d.monitor_dns,
                "monitor_uptime": d.monitor_uptime,
                "check_interval_minutes": d.check_interval_minutes,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "last_checked_at": d.last_checked_at.isoformat() if d.last_checked_at else None,
            }
            for d in domains
        ]

    @staticmethod
    async def get_domain(db: AsyncSession, user: User, domain_id: int) -> Optional[dict]:
        """Get domain details."""
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        domain = result.scalar_one_or_none()
        if domain is None:
            return None

        return {
            "id": domain.id,
            "domain": domain.domain,
            "notes": domain.notes,
            "status": domain.status,
            "monitor_ssl": domain.monitor_ssl,
            "monitor_dns": domain.monitor_dns,
            "monitor_uptime": domain.monitor_uptime,
            "check_interval_minutes": domain.check_interval_minutes,
            "created_at": domain.created_at.isoformat() if domain.created_at else None,
            "updated_at": domain.updated_at.isoformat() if domain.updated_at else None,
            "last_checked_at": domain.last_checked_at.isoformat() if domain.last_checked_at else None,
        }

    @staticmethod
    async def update_domain(
        db: AsyncSession,
        user: User,
        domain_id: int,
        notes: Optional[str] = None,
        status: Optional[str] = None,
        monitor_ssl: Optional[bool] = None,
        monitor_dns: Optional[bool] = None,
        monitor_uptime: Optional[bool] = None,
        check_interval_minutes: Optional[int] = None,
    ) -> Optional[MonitoredDomain]:
        """Update domain settings."""
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        domain = result.scalar_one_or_none()
        if domain is None:
            return None

        if notes is not None:
            domain.notes = notes
        if status is not None:
            domain.status = status
        if monitor_ssl is not None:
            domain.monitor_ssl = monitor_ssl
        if monitor_dns is not None:
            domain.monitor_dns = monitor_dns
        if monitor_uptime is not None:
            domain.monitor_uptime = monitor_uptime
        if check_interval_minutes is not None:
            domain.check_interval_minutes = check_interval_minutes

        domain.updated_at = datetime.utcnow()
        await db.flush()
        return domain

    @staticmethod
    async def delete_domain(db: AsyncSession, user: User, domain_id: int) -> bool:
        """Delete a domain from workspace."""
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        domain = result.scalar_one_or_none()
        if domain is None:
            return False

        await db.delete(domain)
        await db.flush()
        return True

    # ============ Monitoring Data Access ============

    @staticmethod
    async def get_ssl_history(db: AsyncSession, user: User, domain_id: int) -> List[dict]:
        """Get SSL history for a domain."""
        # Verify ownership
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        if result.scalar_one_or_none() is None:
            return []

        result = await db.execute(
            select(DomainSslHistory)
            .where(DomainSslHistory.domain_id == domain_id)
            .order_by(desc(DomainSslHistory.checked_at))
            .limit(50)
        )
        records = result.scalars().all()

        return [
            {
                "id": r.id,
                "issuer": r.issuer,
                "subject": r.subject,
                "valid_from": r.valid_from.isoformat() if r.valid_from else None,
                "valid_until": r.valid_until.isoformat() if r.valid_until else None,
                "days_remaining": r.days_remaining,
                "is_valid": r.is_valid,
                "protocol_version": r.protocol_version,
                "key_type": r.key_type,
                "key_size": r.key_size,
                "checked_at": r.checked_at.isoformat() if r.checked_at else None,
            }
            for r in records
        ]

    @staticmethod
    async def get_dns_history(db: AsyncSession, user: User, domain_id: int) -> List[dict]:
        """Get DNS history for a domain."""
        # Verify ownership
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        if result.scalar_one_or_none() is None:
            return []

        result = await db.execute(
            select(DomainDnsHistory)
            .where(DomainDnsHistory.domain_id == domain_id)
            .order_by(desc(DomainDnsHistory.checked_at))
            .limit(100)
        )
        records = result.scalars().all()

        return [
            {
                "id": r.id,
                "record_type": r.record_type,
                "record_value": r.record_value,
                "ttl": r.ttl,
                "previous_value": r.previous_value,
                "has_changed": r.has_changed,
                "checked_at": r.checked_at.isoformat() if r.checked_at else None,
            }
            for r in records
        ]

    @staticmethod
    async def get_uptime_logs(db: AsyncSession, user: User, domain_id: int) -> List[dict]:
        """Get uptime logs for a domain."""
        # Verify ownership
        result = await db.execute(
            select(MonitoredDomain).where(
                MonitoredDomain.id == domain_id,
                MonitoredDomain.user_id == user.id,
            )
        )
        if result.scalar_one_or_none() is None:
            return []

        # Get uptime check for this domain
        result = await db.execute(
            select(UptimeCheck).where(
                UptimeCheck.domain_id == domain_id,
                UptimeCheck.is_active == True,
            )
        )
        check = result.scalar_one_or_none()
        if check is None:
            return []

        result = await db.execute(
            select(UptimeLog)
            .where(UptimeLog.check_id == check.id)
            .order_by(desc(UptimeLog.checked_at))
            .limit(100)
        )
        logs = result.scalars().all()

        return [
            {
                "id": log.id,
                "is_up": log.is_up,
                "status_code": log.status_code,
                "response_time_ms": log.response_time_ms,
                "error_message": log.error_message,
                "checked_at": log.checked_at.isoformat() if log.checked_at else None,
            }
            for log in logs
        ]

    # ============ Dashboard ============

    @staticmethod
    async def get_dashboard(db: AsyncSession, user: User) -> dict:
        """Get dashboard overview stats."""
        # Count domains
        result = await db.execute(
            select(func.count(MonitoredDomain.id)).where(MonitoredDomain.user_id == user.id)
        )
        total_domains = result.scalar() or 0

        # Count active domains
        result = await db.execute(
            select(func.count(MonitoredDomain.id)).where(
                MonitoredDomain.user_id == user.id,
                MonitoredDomain.status == "active",
            )
        )
        active_domains = result.scalar() or 0

        # Count domains with alerts (SSL expiring soon, DNS changed, etc.)
        # For now, just count domains with status "error"
        result = await db.execute(
            select(func.count(MonitoredDomain.id)).where(
                MonitoredDomain.user_id == user.id,
                MonitoredDomain.status == "error",
            )
        )
        alert_domains = result.scalar() or 0

        return {
            "total_domains": total_domains,
            "active_domains": active_domains,
            "alert_domains": alert_domains,
            "plan": user.plan,
        }
