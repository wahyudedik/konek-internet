"""
Authentication service — register, login, token management.
"""

import re
from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


# Email validation regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class AuthService:
    """Service for user authentication operations."""

    @staticmethod
    def validate_registration(email: str, username: str, password: str) -> Optional[str]:
        """
        Validate registration inputs.
        Returns error message if invalid, None if valid.
        """
        # Email validation
        if not email or not EMAIL_REGEX.match(email):
            return "Format email tidak valid."

        # Username validation
        if not username or len(username) < 3:
            return "Username minimal 3 karakter."
        if len(username) > 50:
            return "Username maksimal 50 karakter."
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return "Username hanya boleh huruf, angka, dan underscore."

        # Password validation
        if not password or len(password) < 8:
            return "Password minimal 8 karakter."
        if len(password) > 128:
            return "Password maksimal 128 karakter."

        return None

    @staticmethod
    async def register(
        db: AsyncSession,
        email: str,
        username: str,
        password: str,
        display_name: Optional[str] = None,
    ) -> Tuple[Optional[dict], Optional[str]]:
        """
        Register a new user.
        
        Returns:
            (token_data, error_message) — one will be None
        """
        # Validate input
        error = AuthService.validate_registration(email, username, password)
        if error:
            return None, error

        # Check email uniqueness
        result = await db.execute(select(User).where(User.email == email.lower()))
        if result.scalar_one_or_none():
            return None, "Email sudah terdaftar."

        # Check username uniqueness
        result = await db.execute(select(User).where(User.username == username.lower()))
        if result.scalar_one_or_none():
            return None, "Username sudah digunakan."

        # Create user
        user = User(
            email=email.lower(),
            username=username.lower(),
            password_hash=hash_password(password),
            display_name=display_name or username,
            is_verified=False,
            is_active=True,
            plan="free",
        )
        db.add(user)
        await db.flush()  # Get user.id

        # Generate tokens
        token_data = AuthService._create_tokens(user)
        return token_data, None

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> Tuple[Optional[dict], Optional[str]]:
        """
        Authenticate user with email and password.
        
        Returns:
            (token_data, error_message) — one will be None
        """
        # Find user
        result = await db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if user is None:
            return None, "Email atau password salah."

        if not user.is_active:
            return None, "Akun tidak aktif. Silakan hubungi support."

        # Verify password
        if not verify_password(password, user.password_hash):
            return None, "Email atau password salah."

        # Update last login
        user.last_login = datetime.utcnow()
        await db.flush()

        # Generate tokens
        token_data = AuthService._create_tokens(user)
        return token_data, None

    @staticmethod
    async def refresh_token(
        db: AsyncSession,
        refresh_token: str,
    ) -> Tuple[Optional[dict], Optional[str]]:
        """
        Refresh access token using refresh token.
        
        Returns:
            (new_token_data, error_message) — one will be None
        """
        payload = decode_token(refresh_token)

        if payload is None:
            return None, "Refresh token tidak valid atau sudah kadaluarsa."

        if payload.get("type") != "refresh":
            return None, "Token bukan refresh token."

        user_id = payload.get("sub")
        if user_id is None:
            return None, "Token tidak valid."

        # Verify user still exists and is active
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()

        if user is None or not user.is_active:
            return None, "User tidak ditemukan atau tidak aktif."

        # Generate new tokens
        token_data = AuthService._create_tokens(user)
        return token_data, None

    @staticmethod
    async def get_user_profile(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user profile by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_profile(
        db: AsyncSession,
        user: User,
        display_name: Optional[str] = None,
    ) -> User:
        """Update user profile."""
        if display_name is not None:
            user.display_name = display_name
        user.updated_at = datetime.utcnow()
        await db.flush()
        return user

    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str,
    ) -> Tuple[bool, Optional[str]]:
        """
        Change user password.
        
        Returns:
            (success, error_message)
        """
        if not verify_password(current_password, user.password_hash):
            return False, "Password saat ini salah."

        if len(new_password) < 8:
            return False, "Password baru minimal 8 karakter."

        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        await db.flush()
        return True, None

    @staticmethod
    def _create_tokens(user: User) -> dict:
        """Generate access and refresh tokens for a user."""
        token_payload = {"sub": str(user.id), "email": user.email, "username": user.username}

        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "display_name": user.display_name,
                "plan": user.plan,
            },
        }
