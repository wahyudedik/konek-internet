"""
Monitored Domain model for workspace domain management.
"""

from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
from app.models.base import Base, TimestampMixin


class MonitoredDomain(Base, TimestampMixin):
    """A domain being monitored by a user."""

    __tablename__ = "monitored_domains"
    __table_args__ = (
        UniqueConstraint("user_id", "domain", name="uq_user_domain"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, paused, error
    monitor_ssl: Mapped[bool] = mapped_column(Boolean, default=True)
    monitor_dns: Mapped[bool] = mapped_column(Boolean, default=True)
    monitor_uptime: Mapped[bool] = mapped_column(Boolean, default=True)
    check_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="monitored_domains")
    ssl_history: Mapped[List["DomainSslHistory"]] = relationship(back_populates="domain", cascade="all, delete-orphan")
    dns_history: Mapped[List["DomainDnsHistory"]] = relationship(back_populates="domain", cascade="all, delete-orphan")
    uptime_checks: Mapped[List["UptimeCheck"]] = relationship(back_populates="domain", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MonitoredDomain(id={self.id}, domain={self.domain}, status={self.status})>"


# Forward references
from app.models.user import User
from app.models.ssl_history import DomainSslHistory
from app.models.dns_history import DomainDnsHistory
from app.models.uptime_check import UptimeCheck
