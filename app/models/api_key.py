"""
API Key model for programmatic access.
"""

from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.models.base import Base, TimestampMixin


class ApiKey(Base, TimestampMixin):
    """API key model for developer access."""

    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(12), nullable=False, index=True)  # kn_abcdefgh
    key_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # SHA-256 hash
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    permissions: Mapped[str] = mapped_column(String(255), default="read")  # read, write, admin
    rate_limit: Mapped[int] = mapped_column(Integer, default=120)  # requests per minute
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="api_keys")

    def __repr__(self):
        return f"<ApiKey(id={self.id}, prefix={self.key_prefix}, name={self.name})>"


# Forward reference
from app.models.user import User
