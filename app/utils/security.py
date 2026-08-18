"""
Security utilities — password hashing, JWT encode/decode, API key generation.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# JWT tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data (must contain "sub" with user_id)
        expires_delta: Custom expiration time
    
    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token with longer expiration.
    
    Args:
        data: Payload data (must contain "sub" with user_id)
    
    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT string
    
    Returns:
        Decoded payload dict or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None


# API Key generation
def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key with kn_ prefix.
    
    Returns:
        Tuple of (full_key, key_hash, key_prefix)
        - full_key: Complete API key (shown to user ONCE)
        - key_hash: SHA-256 hash (stored in database)
        - key_prefix: First 12 chars (used for lookup)
    """
    random_part = secrets.token_urlsafe(24)[:32]
    full_key = f"kn_{random_part}"
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    key_prefix = full_key[:12]  # kn_abcdefgh
    return full_key, key_hash, key_prefix


def verify_api_key(plain_key: str, key_hash: str) -> bool:
    """
    Verify an API key against its hash.
    
    Args:
        plain_key: The plain text API key
        key_hash: The stored SHA-256 hash
    
    Returns:
        True if the key matches
    """
    computed_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return secrets.compare_digest(computed_hash, key_hash)
