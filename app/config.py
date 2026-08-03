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


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()