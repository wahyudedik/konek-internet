import os
from pydantic import BaseModel
from functools import lru_cache


class Settings(BaseModel):
    """Konfigurasi aplikasi Konektivitas.com"""
    
    # App
    APP_NAME: str = os.getenv("APP_NAME", "Konektivitas.com")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION: str = "Platform infrastruktur internet Indonesia yang membantu siapa pun memahami, mengelola, dan mengembangkan aset digital mereka."
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 menit
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "https://konektivitas.com")
    
    # API
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    
    # Database (Fase 2)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./konektivitas.db")
    
    # JWT Authentication (Fase 2)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "konektivitas-dev-secret-change-in-production-2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # SMTP Email (Fase 2)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@konektivitas.com")
    
    # Telegram Bot (Fase 2)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_DEFAULT_CHAT_ID: str = os.getenv("TELEGRAM_DEFAULT_CHAT_ID", "")
    
    # Discord Webhook (Fase 2)
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()