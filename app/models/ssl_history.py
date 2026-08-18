"""
SSL History model for tracking SSL certificate changes.
"""

from sqlalchemy import String, Boolean, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import Optional
from app.models.base import Base


class DomainSslHistory(Base):
    """SSL certificate history for a monitored domain."""

    __tablename__ = "domain_ssl_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id: Mapped[int] = mapped_column(Integer, ForeignKey("monitored_domains.id", ondelete="CASCADE"), nullable=False)
    issuer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    valid_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    san_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # comma-separated SANs
    protocol_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # TLSv1.2, TLSv1.3
    key_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # RSA, ECDSA
    key_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    signature_algorithm: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_valid: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    days_remaining: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    domain: Mapped["MonitoredDomain"] = relationship(back_populates="ssl_history")

    def __repr__(self):
        return f"<DomainSslHistory(domain_id={self.domain_id}, valid_until={self.valid_until}, days={self.days_remaining})>"


# Forward reference
from app.models.monitored_domain import MonitoredDomain
