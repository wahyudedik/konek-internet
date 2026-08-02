import time
import logging
from typing import Optional
from fastapi import Request, HTTPException

logger = logging.getLogger("konektivitas.rate_limit")

# In-memory rate limiting (per-IP)
_rate_limits: dict = {}
WINDOW_SIZE = 60  # 1 menit
MAX_REQUESTS = 60  # 60 request per menit per IP
_CLEANUP_INTERVAL = 300  # Cleanup setiap 5 menit
_last_cleanup: float = 0.0


def get_client_ip(request: Request) -> str:
    """Get client IP from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _maybe_cleanup():
    """Periodic cleanup - max sekali per 5 menit"""
    global _last_cleanup
    now = time.time()
    if now - _last_cleanup < _CLEANUP_INTERVAL:
        return
    _last_cleanup = now
    
    before = len(_rate_limits)
    empty_ips = []
    
    for ip, timestamps in _rate_limits.items():
        recent = [t for t in timestamps if now - t < WINDOW_SIZE]
        if recent:
            _rate_limits[ip] = recent
        else:
            empty_ips.append(ip)
    
    for ip in empty_ips:
        del _rate_limits[ip]
    
    after = len(_rate_limits)
    if before != after:
        logger.debug("Rate limit cleanup: %d -> %d IPs", before, after)


def check_rate_limit(ip: str, max_requests: int = MAX_REQUESTS) -> bool:
    """Check if IP has exceeded rate limit. Returns True if allowed."""
    _maybe_cleanup()
    now = time.time()
    
    if ip not in _rate_limits:
        _rate_limits[ip] = []
    
    # Remove old entries outside window
    _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < WINDOW_SIZE]
    
    if len(_rate_limits[ip]) >= max_requests:
        logger.warning("Rate limit exceeded for IP: %s", ip)
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
    """Manual cleanup - dipanggil dari scheduled task"""
    global _last_cleanup
    _last_cleanup = 0.0  # Force cleanup
    _maybe_cleanup()