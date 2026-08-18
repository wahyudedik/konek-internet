"""
Notification API endpoints — manage notification settings (Email, Telegram, Discord).
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ============ Request/Response Models ============

class AddNotificationRequest(BaseModel):
    channel: str  # email, telegram, discord
    config: Optional[dict] = None


class ToggleNotificationRequest(BaseModel):
    enabled: bool


class NotificationInfo(BaseModel):
    id: int
    channel: str
    is_enabled: bool
    config: dict
    created_at: Optional[str]


class MessageResponse(BaseModel):
    message: str


# ============ Endpoints ============

@router.get("/", response_model=List[NotificationInfo])
async def list_notifications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all notification settings for the user."""
    return await NotificationService.get_user_notifications(db=db, user_id=user.id)


@router.post("/", response_model=NotificationInfo, status_code=status.HTTP_201_CREATED)
async def add_notification(
    request: AddNotificationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add or update a notification channel."""
    try:
        result = await NotificationService.add_notification_setting(
            db=db,
            user_id=user.id,
            channel=request.channel,
            config=request.config,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    await db.commit()
    return result


@router.put("/{channel}/toggle", response_model=MessageResponse)
async def toggle_notification(
    channel: str,
    request: ToggleNotificationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Enable or disable a notification channel."""
    success = await NotificationService.toggle_notification(
        db=db,
        user_id=user.id,
        channel=channel,
        enabled=request.enabled,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notifikasi channel '{channel}' tidak ditemukan.",
        )

    await db.commit()
    status_text = "diaktifkan" if request.enabled else "dinonaktifkan"
    return MessageResponse(message=f"Notifikasi {channel} berhasil {status_text}.")


@router.delete("/{channel}", response_model=MessageResponse)
async def delete_notification(
    channel: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a notification channel."""
    success = await NotificationService.delete_notification(
        db=db,
        user_id=user.id,
        channel=channel,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notifikasi channel '{channel}' tidak ditemukan.",
        )

    await db.commit()
    return MessageResponse(message=f"Notifikasi {channel} berhasil dihapus.")
