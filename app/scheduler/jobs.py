"""
Background scheduler for automated monitoring checks.

Uses APScheduler for periodic SSL, DNS, and Uptime checks.
Runs as an async task within the FastAPI application lifecycle.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.monitored_domain import MonitoredDomain
from app.services.monitoring_service import MonitoringService
from app.services.notification_service import NotificationService

logger = logging.getLogger("konektivitas.scheduler")


class MonitoringScheduler:
    """
    Background scheduler that runs monitoring checks at configured intervals.
    
    Instead of APScheduler (heavy dependency), uses a simple async loop
    that checks domains based on their check_interval_minutes setting.
    """

    def __init__(self):
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self):
        """Start the background monitoring loop."""
        if self._running:
            logger.warning("Scheduler already running.")
            return

        self._running = True
        self._task = asyncio.create_task(self._monitoring_loop())
        logger.info("Monitoring scheduler started.")

    async def stop(self):
        """Stop the background monitoring loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Monitoring scheduler stopped.")

    async def _monitoring_loop(self):
        """Main monitoring loop — checks domains at their configured intervals."""
        while self._running:
            try:
                await self._run_check_cycle()
            except Exception as e:
                logger.error("Error in monitoring cycle: %s", str(e))

            # Wait 60 seconds before next cycle
            try:
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                break

    async def _run_check_cycle(self):
        """Run one cycle of monitoring checks for all due domains."""
        async with async_session_factory() as db:
            try:
                # Find domains that need checking
                now = datetime.utcnow()
                result = await db.execute(
                    select(MonitoredDomain).where(
                        MonitoredDomain.status == "active",
                    )
                )
                domains = result.scalars().all()

                checked_count = 0

                for domain in domains:
                    # Check if this domain is due for checking
                    if domain.last_checked_at is None:
                        is_due = True
                    else:
                        interval = timedelta(minutes=domain.check_interval_minutes)
                        is_due = (now - domain.last_checked_at) >= interval

                    if not is_due:
                        continue

                    logger.info("Running checks for %s (interval: %d min)", 
                              domain.domain, domain.check_interval_minutes)

                    check_results = {}

                    # SSL check
                    if domain.monitor_ssl:
                        ssl_result = await MonitoringService.check_ssl(db, domain.id)
                        if ssl_result:
                            check_results["ssl"] = ssl_result

                    # DNS check
                    if domain.monitor_dns:
                        dns_result = await MonitoringService.check_dns(db, domain.id)
                        if dns_result:
                            check_results["dns"] = dns_result

                    # Uptime check
                    if domain.monitor_uptime:
                        uptime_result = await MonitoringService.check_uptime(db, domain.id)
                        if uptime_result:
                            check_results["uptime"] = uptime_result

                    # Send notifications if there are issues
                    if check_results:
                        await self._handle_notifications(db, domain, check_results)

                    checked_count += 1

                if checked_count > 0:
                    await db.commit()
                    logger.info("Monitoring cycle complete. Checked %d domains.", checked_count)

            except Exception as e:
                logger.error("Error in check cycle: %s", str(e))
                await db.rollback()

    async def _handle_notifications(self, db: AsyncSession, domain: MonitoredDomain, results: dict):
        """Handle notifications for monitoring results (issues detected)."""
        try:
            # Check for SSL issues
            ssl_data = results.get("ssl")
            if ssl_data:
                days = ssl_data.get("days_remaining")
                if days is not None and days <= 30:
                    await NotificationService.send_notification(
                        db=db,
                        user_id=domain.user_id,
                        event="ssl_expiring",
                        domain=domain.domain,
                        message=f"SSL certificate untuk {domain.domain} akan kadaluarsa dalam {days} hari.",
                        data=ssl_data,
                    )

            # Check for uptime issues
            uptime_data = results.get("uptime")
            if uptime_data:
                if not uptime_data.get("is_up"):
                    await NotificationService.send_notification(
                        db=db,
                        user_id=domain.user_id,
                        event="domain_down",
                        domain=domain.domain,
                        message=f"Domain {domain.domain} tidak dapat diakses! Error: {uptime_data.get('error_message', 'Unknown')}",
                        data=uptime_data,
                    )

            # Check for DNS changes
            dns_data = results.get("dns")
            if dns_data:
                changes = dns_data.get("changes_detected", [])
                if changes:
                    change_summary = ", ".join([f"{c['type']}={c['value']}" for c in changes])
                    await NotificationService.send_notification(
                        db=db,
                        user_id=domain.user_id,
                        event="dns_change",
                        domain=domain.domain,
                        message=f"DNS record berubah untuk {domain.domain}: {change_summary}",
                        data=dns_data,
                    )

        except Exception as e:
            logger.error("Error sending notifications for %s: %s", domain.domain, str(e))


# Global scheduler instance
scheduler = MonitoringScheduler()
