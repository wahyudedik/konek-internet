"""Dynamic DNS model - Menyimpan konfigurasi DDNS per pengguna"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.models.base import Base


class DynamicDns(Base):
    """
    Dynamic DNS record - Konfigurasi DDNS per domain/hostname.
    
    Pengguna bisa mendaftarkan hostname yang akan otomatis update
    IP-nya melalui API endpoint yang simpel.
    """
    __tablename__ = "dynamic_dns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Domain config
    hostname = Column(String(255), nullable=False)  # e.g. "home.example.com"
    domain = Column(String(255), nullable=False)     # e.g. "example.com"
    record_type = Column(String(10), default="A")    # A, AAAA
    
    # Auth token (unik per record)
    token = Column(String(64), nullable=False, unique=True, index=True)
    
    # Provider config (cloudflare, etc)
    provider = Column(String(50), default="manual")  # manual, cloudflare
    provider_config = Column(Text, nullable=True)     # JSON: {"zone_id": "...", "record_id": "...", "api_token": "..."}
    
    # Current state
    current_ip = Column(String(45), nullable=True)    # IPv4 atau IPv6
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Settings
    is_active = Column(Boolean, default=True)
    update_interval_minutes = Column(Integer, default=5)  # Minimum interval antar update
    ttl = Column(Integer, default=300)                     # DNS TTL dalam detik
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<DynamicDns {self.hostname} -> {self.current_ip}>"
