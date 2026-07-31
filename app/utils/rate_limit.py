import time
from typing import Optional
from fastapi import Request, HTTPException

# In-memory rate limiting (per-IP)
_rate_limits: dict = {}
WINDOW_SIZE = 60  # 1 menit
MAX_REQUESTS = 60  # 60 request per menit per IP


def get_client_ip(request: Request) -> str:
    """Get client IP from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(ip: str, max_requests: int = MAX_REQUESTS) -> bool:
    """Check if IP has exceeded rate limit. Returns True if allowed."""
    now = time.time()
    
    if ip not in _rate_limits:
        _rate_limits[ip] = []
    
    # Remove old entries outside window
    _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < WINDOW_SIZE]
    
    if len(_rate_limits[ip]) >= max_requests:
        return False
    
    _rate_limits[ip].append(now)
    return True


def get_remaining_requests(ip: str, max_requests: int = MAX_REQUESTS) -> int:
    """Get remaining requests for IP"""
    now = time.time()
    
    if ip not in _rate_limits:
        return max_requests
    
    recent = [t for t in _rate_limits[ip] if now - t < WINDOW_SIZE]
    return max(0, max_requests - len(recent))


def cleanup_old_entries():
    """Cleanup old rate limit entries (call periodically)"""
    now = time.time()
    empty_ips = []
    
    for ip, timestamps in _rate_limits.items():
        _rate_limits[ip] = [t for t in timestamps if now - t < WINDOW_SIZE]
        if not _rate_limits[ip]:
            empty_ips.append(ip)
    
    for ip in empty_ips:
        del _rate_limits[ip]