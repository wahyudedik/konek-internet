"""
Notification service — sends alerts via Email, Telegram, Discord.

Supports:
- Email (SMTP)
- Telegram Bot API
- Discord Webhook
"""

import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict
from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.notification import NotificationSetting
from app.models.user import User

settings = get_settings()

logger = logging.getLogger("konektivitas.notification")


class NotificationService:
    """Service for sending notifications via configured channels."""

    @staticmethod
    async def send_notification(
        db: AsyncSession,
        user_id: int,
        event: str,
        domain: str,
        message: str,
        data: Optional[dict] = None,
    ) -> List[dict]:
        """
        Send notification to all enabled channels for a user.

        Args:
            db: Database session
            user_id: User ID to notify
            event: Event type (ssl_expiring, domain_down, dns_change, etc.)
            domain: Domain name affected
            message: Notification message
            data: Additional data (check results)

        Returns:
            List of delivery results
        """
        # Get user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return []

        # Get enabled notification settings
        result = await db.execute(
            select(NotificationSetting).where(
                NotificationSetting.user_id == user_id,
                NotificationSetting.is_enabled == True,
            )
        )
        settings_list = result.scalars().all()

        results = []

        for setting in settings_list:
            try:
                if setting.channel == "email":
                    result = await NotificationService._send_email(
                        user=user,
                        event=event,
                        domain=domain,
                        message=message,
                        data=data,
                    )
                elif setting.channel == "telegram":
                    config = json.loads(setting.config_json) if setting.config_json else {}
                    result = await NotificationService._send_telegram(
                        bot_token=config.get("bot_token"),
                        chat_id=config.get("chat_id"),
                        event=event,
                        domain=domain,
                        message=message,
                        data=data,
                    )
                elif setting.channel == "discord":
                    config = json.loads(setting.config_json) if setting.config_json else {}
                    result = await NotificationService._send_discord(
                        webhook_url=config.get("webhook_url"),
                        event=event,
                        domain=domain,
                        message=message,
                        data=data,
                    )
                else:
                    continue

                results.append({
                    "channel": setting.channel,
                    "success": result.get("success", False),
                    "error": result.get("error"),
                })

            except Exception as e:
                logger.error("Failed to send %s notification: %s", setting.channel, str(e))
                results.append({
                    "channel": setting.channel,
                    "success": False,
                    "error": str(e),
                })

        return results

    @staticmethod
    async def _send_email(
        user: User,
        event: str,
        domain: str,
        message: str,
        data: Optional[dict] = None,
    ) -> dict:
        """Send email notification via SMTP."""
        smtp_host = settings.SMTP_HOST
        smtp_port = settings.SMTP_PORT
        smtp_user = settings.SMTP_USER
        smtp_pass = settings.SMTP_PASSWORD
        from_email = settings.SMTP_FROM or smtp_user

        if not all([smtp_host, smtp_user, smtp_pass]):
            return {"success": False, "error": "SMTP not configured"}

        # Build email
        event_labels = {
            "ssl_expiring": "⚠️ SSL Certificate Expiring",
            "domain_down": "🔴 Domain Down",
            "dns_change": "🔄 DNS Record Changed",
            "uptime_restored": "🟢 Domain Restored",
        }

        subject = f"[Konektivitas] {event_labels.get(event, event)} — {domain}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; color: white; padding: 20px; text-align: center;">
                <h2 style="margin: 0;">Konektivitas.com</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">Monitoring Alert</p>
            </div>
            <div style="padding: 20px; background: #f8f9fa;">
                <h3>{event_labels.get(event, event)}</h3>
                <p><strong>Domain:</strong> {domain}</p>
                <p><strong>Pesan:</strong> {message}</p>
                <p><strong>Waktu:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                {"<p><strong>Detail:</strong></p><pre style='background:#fff;padding:10px;border-radius:4px;overflow-x:auto;'>" + json.dumps(data, indent=2) + "</pre>" if data else ""}
            </div>
            <div style="padding: 10px 20px; background: #e9ecef; text-align: center; font-size: 12px; color: #666;">
                <p>Ini adalah notifikasi otomatis dari Konektivitas.com monitoring.</p>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Konektivitas <{from_email}>"
        msg["To"] = user.email
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, user.email, msg.as_string())

            logger.info("Email notification sent to %s for %s", user.email, domain)
            return {"success": True, "error": None}

        except Exception as e:
            logger.error("Email send failed: %s", str(e))
            return {"success": False, "error": str(e)}

    @staticmethod
    async def _send_telegram(
        bot_token: Optional[str],
        chat_id: Optional[str],
        event: str,
        domain: str,
        message: str,
        data: Optional[dict] = None,
    ) -> dict:
        """Send Telegram notification via Bot API."""
        if not bot_token or not chat_id:
            return {"success": False, "error": "Telegram not configured"}

        event_emojis = {
            "ssl_expiring": "⚠️",
            "domain_down": "🔴",
            "dns_change": "🔄",
            "uptime_restored": "🟢",
        }

        emoji = event_emojis.get(event, "📢")
        text = (
            f"{emoji} *Konektivitas Monitoring*\n\n"
            f"*Domain:* {domain}\n"
            f"*Event:* {event}\n"
            f"*Pesan:* {message}\n"
            f"*Waktu:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload)

            if resp.status_code == 200:
                logger.info("Telegram notification sent for %s", domain)
                return {"success": True, "error": None}
            else:
                error = resp.text
                logger.error("Telegram API error: %s", error)
                return {"success": False, "error": error}

        except Exception as e:
            logger.error("Telegram send failed: %s", str(e))
            return {"success": False, "error": str(e)}

    @staticmethod
    async def _send_discord(
        webhook_url: Optional[str],
        event: str,
        domain: str,
        message: str,
        data: Optional[dict] = None,
    ) -> dict:
        """Send Discord notification via Webhook."""
        if not webhook_url:
            return {"success": False, "error": "Discord webhook not configured"}

        event_colors = {
            "ssl_expiring": 0xFFA500,  # Orange
            "domain_down": 0xFF0000,  # Red
            "dns_change": 0x00AAFF,  # Blue
            "uptime_restored": 0x00FF00,  # Green
        }

        embed = {
            "title": f"Konektivitas Monitoring — {domain}",
            "description": message,
            "color": event_colors.get(event, 0x808080),
            "fields": [
                {"name": "Domain", "value": domain, "inline": True},
                {"name": "Event", "value": event, "inline": True},
                {"name": "Waktu", "value": datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'), "inline": False},
            ],
            "footer": {
                "text": "Konektivitas.com Monitoring"
            }
        }

        if data:
            data_str = json.dumps(data, indent=2)
            if len(data_str) > 1024:
                data_str = data_str[:1020] + "..."
            embed["fields"].append({
                "name": "Detail",
                "value": f"```{data_str}```",
                "inline": False,
            })

        payload = {"embeds": [embed]}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(webhook_url, json=payload)

            if resp.status_code in (200, 204):
                logger.info("Discord notification sent for %s", domain)
                return {"success": True, "error": None}
            else:
                error = resp.text
                logger.error("Discord webhook error: %s", error)
                return {"success": False, "error": error}

        except Exception as e:
            logger.error("Discord send failed: %s", str(e))
            return {"success": False, "error": str(e)}

    @staticmethod
    async def get_user_notifications(db: AsyncSession, user_id: int) -> List[dict]:
        """Get notification settings for a user."""
        result = await db.execute(
            select(NotificationSetting).where(
                NotificationSetting.user_id == user_id,
            )
        )
        settings_list = result.scalars().all()

        return [
            {
                "id": s.id,
                "channel": s.channel,
                "is_enabled": s.is_enabled,
                "config": json.loads(s.config_json) if s.config_json else {},
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in settings_list
        ]

    @staticmethod
    async def add_notification_setting(
        db: AsyncSession,
        user_id: int,
        channel: str,
        config: Optional[dict] = None,
    ) -> dict:
        """Add or update a notification setting."""
        if channel not in ("email", "telegram", "discord"):
            raise ValueError("Channel harus email, telegram, atau discord.")

        # Check existing
        result = await db.execute(
            select(NotificationSetting).where(
                NotificationSetting.user_id == user_id,
                NotificationSetting.channel == channel,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.is_enabled = True
            if config is not None:
                existing.config_json = json.dumps(config)
            setting = existing
        else:
            setting = NotificationSetting(
                user_id=user_id,
                channel=channel,
                is_enabled=True,
                config_json=json.dumps(config) if config else None,
            )
            db.add(setting)

        await db.flush()

        return {
            "id": setting.id,
            "channel": setting.channel,
            "is_enabled": setting.is_enabled,
            "config": json.loads(setting.config_json) if setting.config_json else {},
        }

    @staticmethod
    async def toggle_notification(
        db: AsyncSession,
        user_id: int,
        channel: str,
        enabled: bool,
    ) -> bool:
        """Toggle a notification channel on/off."""
        result = await db.execute(
            select(NotificationSetting).where(
                NotificationSetting.user_id == user_id,
                NotificationSetting.channel == channel,
            )
        )
        setting = result.scalar_one_or_none()
        if setting is None:
            return False

        setting.is_enabled = enabled
        await db.flush()
        return True

    @staticmethod
    async def delete_notification(
        db: AsyncSession,
        user_id: int,
        channel: str,
    ) -> bool:
        """Delete a notification setting."""
        result = await db.execute(
            select(NotificationSetting).where(
                NotificationSetting.user_id == user_id,
                NotificationSetting.channel == channel,
            )
        )
        setting = result.scalar_one_or_none()
        if setting is None:
            return False

        await db.delete(setting)
        await db.flush()
        return True
