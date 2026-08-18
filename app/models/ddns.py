"""
Dynamic DNS model — Menyimpan konfigurasi DDNS per pengguna.
"""

from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.models.base import Base, TimestampMixin


class DynamicDns(Base, TimestampMixin):
    """
    Dynamic DNS record — Konfigurasi DDNS per domain/hostname.

    Pengguna bisa mendaftarkan hostname yang akan otomatis update
    IP-nya melalui API endpoint yang simpel.
    """
    __tablename__ = "dynamic_dns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Domain config
    hostname: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g. "home.example.com"
    domain: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g. "example.com"
    record_type: Mapped[str] = mapped_column(String(10), default="A")  # A, AAAA

    # Auth token (unik per record)
    token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    # Provider config (cloudflare, etc)
    provider: Mapped[str] = mapped_column(String(50), default="manual")  # manual, cloudflare
    provider_config: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON: {"zone_id": "...", "record_id": "...", "api_token": "..."}

    # Current state
    current_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv4 atau IPv6
    last_updated: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    update_interval_minutes: Mapped[int] = mapped_column(Integer, default=5)  # Minimum interval antar update
    ttl: Mapped[int] = mapped_column(Integer, default=300)  # DNS TTL dalam detik

    def __repr__(self):
        return f"<DynamicDns {self.hostname} -> {self.current_ip}>"


# Forward reference
from app.models.user import User
