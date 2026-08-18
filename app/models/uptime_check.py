"""
Uptime Check & Log models for website monitoring.
"""

from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
from app.models.base import Base, TimestampMixin


class UptimeCheck(Base, TimestampMixin):
    """Uptime check configuration for a monitored domain."""

    __tablename__ = "uptime_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id: Mapped[int] = mapped_column(Integer, ForeignKey("monitored_domains.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    method: Mapped[str] = mapped_column(String(10), default="GET")
    expected_status: Mapped[int] = mapped_column(Integer, default=200)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=10)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    domain: Mapped["MonitoredDomain"] = relationship(back_populates="uptime_checks")
    logs: Mapped[List["UptimeLog"]] = relationship(back_populates="check", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UptimeCheck(id={self.id}, url={self.url}, active={self.is_active})>"


class UptimeLog(Base):
    """Individual uptime check result."""

    __tablename__ = "uptime_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_id: Mapped[int] = mapped_column(Integer, ForeignKey("uptime_checks.id", ondelete="CASCADE"), nullable=False)
    is_up: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_from: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    check: Mapped["UptimeCheck"] = relationship(back_populates="logs")

    def __repr__(self):
        return f"<UptimeLog(check_id={self.check_id}, up={self.is_up}, time={self.response_time_ms}ms)>"


# Forward reference
from app.models.monitored_domain import MonitoredDomain
