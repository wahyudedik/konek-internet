"""
Monitoring service — performs SSL, DNS, Uptime checks and stores results in DB.
Reuses existing services (ssl_service, dns_service, website_service).
"""

import asyncio
import logging
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.monitored_domain import MonitoredDomain
from app.models.ssl_history import DomainSslHistory
from app.models.dns_history import DomainDnsHistory
from app.models.uptime_check import UptimeCheck, UptimeLog

logger = logging.getLogger("konektivitas.monitoring")


class MonitoringService:
    """Service for performing and storing monitoring checks."""

    @staticmethod
    async def check_ssl(db: AsyncSession, domain_id: int) -> Optional[dict]:
        """
        Perform SSL check for a monitored domain and store result.
        Uses existing ssl_service.
        """
        from app.services.ssl_service import check_ssl

        # Get domain
        result = await db.execute(
            select(MonitoredDomain).where(MonitoredDomain.id == domain_id)
        )
        domain = result.scalar_one_or_none()
        if domain is None or not domain.monitor_ssl:
            return None

        try:
            # Use existing SSL service (check_ssl returns: valid, not_before, not_after,
            # issuer dict, subject dict, subject_alt_names list, serial_number, etc.)
            ssl_data = await check_ssl(domain.domain)
        except Exception as e:
            logger.error("SSL check failed for %s: %s", domain.domain, str(e))
            return None

        if not ssl_data or ssl_data.get("error"):
            logger.warning("SSL check returned error for %s: %s", domain.domain, ssl_data.get("error"))
            return None

        # Parse dates — check_ssl returns "not_before" and "not_after" strings
        valid_from = None
        valid_until = None
        days_remaining = None

        if ssl_data.get("not_before"):
            try:
                valid_from = datetime.strptime(ssl_data["not_before"], "%b %d %H:%M:%S %Y %Z").date()
            except (ValueError, TypeError):
                pass

        if ssl_data.get("not_after"):
            try:
                valid_until = datetime.strptime(ssl_data["not_after"], "%b %d %H:%M:%S %Y %Z").date()
                days_remaining = (valid_until - date.today()).days
            except (ValueError, TypeError):
                pass

        # Extract issuer/subject strings from dicts returned by check_ssl
        issuer_raw = ssl_data.get("issuer", {})
        issuer_str = issuer_raw.get("organizationName", "") if isinstance(issuer_raw, dict) else str(issuer_raw)

        subject_raw = ssl_data.get("subject", {})
        subject_str = subject_raw.get("commonName", "") if isinstance(subject_raw, dict) else str(subject_raw)

        # Store in DB
        ssl_record = DomainSslHistory(
            domain_id=domain_id,
            issuer=issuer_str or None,
            subject=subject_str or None,
            serial_number=ssl_data.get("serial_number"),
            valid_from=valid_from,
            valid_until=valid_until,
            san_list=",".join(ssl_data.get("subject_alt_names", [])) if ssl_data.get("subject_alt_names") else None,
            protocol_version=ssl_data.get("protocol_version"),
            key_type=ssl_data.get("key_type"),
            key_size=ssl_data.get("key_size"),
            signature_algorithm=ssl_data.get("signature_algorithm"),
            is_valid=ssl_data.get("valid", True),
            days_remaining=days_remaining,
        )
        db.add(ssl_record)

        # Update domain last_checked_at
        domain.last_checked_at = datetime.utcnow()
        await db.flush()

        return {
            "domain": domain.domain,
            "is_valid": ssl_record.is_valid,
            "days_remaining": ssl_record.days_remaining,
            "valid_until": str(valid_until) if valid_until else None,
        }

    @staticmethod
    async def check_dns(db: AsyncSession, domain_id: int) -> Optional[dict]:
        """
        Perform DNS check for a monitored domain and store results.
        Uses existing dns_service.
        """
        from app.services.dns_service import lookup_dns

        # Get domain
        result = await db.execute(
            select(MonitoredDomain).where(MonitoredDomain.id == domain_id)
        )
        domain = result.scalar_one_or_none()
        if domain is None or not domain.monitor_dns:
            return None

        # Get previous DNS records for comparison
        result = await db.execute(
            select(DomainDnsHistory)
            .where(DomainDnsHistory.domain_id == domain_id)
            .order_by(desc(DomainDnsHistory.checked_at))
            .limit(50)
        )
        previous_records = result.scalars().all()

        # Build previous state: {type: [values]}
        previous_state = {}
        for rec in previous_records:
            key = rec.record_type
            if key not in previous_state:
                previous_state[key] = set()
            previous_state[key].add(rec.record_value)

        changes_detected = []
        new_records = []

        try:
            # lookup_dns() returns {"domain": str, "record_type": str, "records": [str, ...], "error": str|None}
            for record_type in ["A", "MX", "NS"]:
                dns_result = await lookup_dns(domain.domain, record_type)
                if not dns_result or dns_result.get("error"):
                    continue
                records_list = dns_result.get("records", [])
                for record_value in records_list:
                    value = str(record_value)
                    has_changed = value not in previous_state.get(record_type, set())
                    if has_changed and record_type == "A":
                        changes_detected.append({"type": record_type, "value": value})

                    dns_record = DomainDnsHistory(
                        domain_id=domain_id,
                        record_type=record_type,
                        record_value=value,
                        previous_value=list(previous_state.get(record_type, {None}))[0] if previous_state.get(record_type) else None,
                        has_changed=has_changed,
                    )
                    db.add(dns_record)
                    new_records.append(dns_record)

        except Exception as e:
            logger.error("DNS check failed for %s: %s", domain.domain, str(e))
            return None

        # Update domain
        domain.last_checked_at = datetime.utcnow()
        await db.flush()

        return {
            "domain": domain.domain,
            "records_checked": len(new_records),
            "changes_detected": changes_detected,
        }

    @staticmethod
    async def check_uptime(db: AsyncSession, domain_id: int) -> Optional[dict]:
        """
        Perform uptime check for a monitored domain and store result.
        Uses existing website_service for HTTP check.
        """
        import httpx

        # Get domain and uptime check config
        result = await db.execute(
            select(MonitoredDomain).where(MonitoredDomain.id == domain_id)
        )
        domain = result.scalar_one_or_none()
        if domain is None or not domain.monitor_uptime:
            return None

        result = await db.execute(
            select(UptimeCheck).where(
                UptimeCheck.domain_id == domain_id,
                UptimeCheck.is_active == True,
            )
        )
        check = result.scalar_one_or_none()
        if check is None:
            return None

        # Perform HTTP check
        is_up = False
        status_code = None
        response_time_ms = None
        error_message = None

        try:
            async with httpx.AsyncClient(timeout=check.timeout_seconds, follow_redirects=True) as client:
                response = await client.request(
                    method=check.method,
                    url=check.url,
                )
                status_code = response.status_code
                response_time_ms = int(response.elapsed.total_seconds() * 1000)
                is_up = response.status_code == check.expected_status or 200 <= response.status_code < 400
        except httpx.TimeoutException:
            error_message = "Connection timeout"
        except httpx.ConnectError as e:
            error_message = f"Connection failed: {str(e)}"
        except Exception as e:
            error_message = f"Check failed: {str(e)}"

        # Store log
        uptime_log = UptimeLog(
            check_id=check.id,
            is_up=is_up,
            status_code=status_code,
            response_time_ms=response_time_ms,
            error_message=error_message,
            checked_from="server",
        )
        db.add(uptime_log)

        # Update domain status based on uptime
        if not is_up:
            domain.status = "error"
        elif domain.status == "error":
            domain.status = "active"

        domain.last_checked_at = datetime.utcnow()
        await db.flush()

        return {
            "domain": domain.domain,
            "is_up": is_up,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "error_message": error_message,
        }

    @staticmethod
    async def run_all_checks(db: AsyncSession) -> List[dict]:
        """
        Run all monitoring checks for all active domains.
        Called by the scheduler.
        """
        results = []

        result = await db.execute(
            select(MonitoredDomain).where(MonitoredDomain.status == "active")
        )
        domains = result.scalars().all()

        for domain in domains:
            domain_results = {}

            # SSL check
            if domain.monitor_ssl:
                ssl_result = await MonitoringService.check_ssl(db, domain.id)
                if ssl_result:
                    domain_results["ssl"] = ssl_result

            # DNS check
            if domain.monitor_dns:
                dns_result = await MonitoringService.check_dns(db, domain.id)
                if dns_result:
                    domain_results["dns"] = dns_result

            # Uptime check
            if domain.monitor_uptime:
                uptime_result = await MonitoringService.check_uptime(db, domain.id)
                if uptime_result:
                    domain_results["uptime"] = uptime_result

            if domain_results:
                results.append(domain_results)

        await db.commit()
        return results
