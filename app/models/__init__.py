"""
Models package — import all models for Alembic discovery.
"""

from app.models.base import Base
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.monitored_domain import MonitoredDomain
from app.models.ssl_history import DomainSslHistory
from app.models.dns_history import DomainDnsHistory
from app.models.uptime_check import UptimeCheck, UptimeLog
from app.models.notification import NotificationSetting
from app.models.ddns import DynamicDns

__all__ = [
    "Base",
    "User",
    "ApiKey",
    "MonitoredDomain",
    "DomainSslHistory",
    "DomainDnsHistory",
    "UptimeCheck",
    "UptimeLog",
    "NotificationSetting",
    "DynamicDns",
]
