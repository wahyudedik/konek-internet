"""
Authentication API endpoints — register, login, refresh, profile.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============ Request/Response Models ============

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    display_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: dict


class MessageResponse(BaseModel):
    message: str


class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    display_name: Optional[str]
    plan: str
    is_verified: bool
    created_at: str
    last_login: Optional[str]


# ============ Endpoints ============

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    token_data, error = await AuthService.register(
        db=db,
        email=request.email,
        username=request.username,
        password=request.password,
        display_name=request.display_name,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return token_data


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    token_data, error = await AuthService.login(
        db=db,
        email=request.email,
        password=request.password,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
        )

    return token_data


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Get new access token using refresh token."""
    token_data, error = await AuthService.refresh_token(
        db=db,
        refresh_token=request.refresh_token,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
        )

    return token_data


@router.get("/me", response_model=UserProfile)
async def get_profile(user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserProfile(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        plan=user.plan,
        is_verified=user.is_verified,
        created_at=user.created_at.isoformat() if user.created_at else "",
        last_login=user.last_login.isoformat() if user.last_login else None,
    )


@router.put("/me", response_model=UserProfile)
async def update_profile(
    request: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile."""
    updated_user = await AuthService.update_profile(
        db=db,
        user=user,
        display_name=request.display_name,
    )

    return UserProfile(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        display_name=updated_user.display_name,
        plan=updated_user.plan,
        is_verified=updated_user.is_verified,
        created_at=updated_user.created_at.isoformat() if updated_user.created_at else "",
        last_login=updated_user.last_login.isoformat() if updated_user.last_login else None,
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change current user password."""
    success, error = await AuthService.change_password(
        db=db,
        user=user,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return MessageResponse(message="Password berhasil diubah.")
