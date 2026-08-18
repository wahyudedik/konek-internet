"""
DNS History model for tracking DNS record changes.
"""

from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.models.base import Base


class DomainDnsHistory(Base):
    """DNS record history for a monitored domain."""

    __tablename__ = "domain_dns_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id: Mapped[int] = mapped_column(Integer, ForeignKey("monitored_domains.id", ondelete="CASCADE"), nullable=False)
    record_type: Mapped[str] = mapped_column(String(10), nullable=False)  # A, AAAA, MX, CNAME, TXT, NS
    record_value: Mapped[str] = mapped_column(Text, nullable=False)
    ttl: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    previous_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # NULL if first check
    has_changed: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    domain: Mapped["MonitoredDomain"] = relationship(back_populates="dns_history")

    def __repr__(self):
        return f"<DomainDnsHistory(domain_id={self.domain_id}, type={self.record_type}, changed={self.has_changed})>"


# Forward reference
from app.models.monitored_domain import MonitoredDomain
