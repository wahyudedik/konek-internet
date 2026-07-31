from pydantic import BaseModel
from functools import lru_cache


class Settings(BaseModel):
    """Konfigurasi aplikasi Konektivitas.com"""
    
    # App
    APP_NAME: str = "Konektivitas.com"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Infrastruktur Internet Gratis untuk Indonesia"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300  # 5 menit
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # API
    API_V1_PREFIX: str = "/api/v1"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()