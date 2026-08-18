"""
Notification Settings model for user alert preferences.
"""

from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.models.base import Base, TimestampMixin


class NotificationSetting(Base, TimestampMixin):
    """User notification channel configuration."""

    __tablename__ = "notification_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "channel", name="uq_user_channel"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)  # email, telegram, discord
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # channel-specific config

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notification_settings")

    def __repr__(self):
        return f"<NotificationSetting(user_id={self.user_id}, channel={self.channel}, enabled={self.is_enabled})>"


# Forward reference
from app.models.user import User
