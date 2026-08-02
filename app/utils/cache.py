import json
import hashlib
import time
import logging
from typing import Optional, Callable
from functools import wraps

logger = logging.getLogger("konektivitas.cache")

# In-memory cache fallback (ketika Redis tidak tersedia)
_memory_cache: dict = {}
_memory_cache_ttl: dict = {}
_CACHE_CLEANUP_INTERVAL = 300  # Cleanup setiap 5 menit
_last_cache_cleanup: float = 0.0


def _get_redis():
    """Try to connect to Redis, return None if unavailable"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
        r.ping()
        return r
    except Exception:
        return None


_redis_client = None


def _cleanup_expired_cache():
    """Periodic cleanup of expired in-memory cache entries"""
    global _last_cache_cleanup
    now = time.time()
    if now - _last_cache_cleanup < _CACHE_CLEANUP_INTERVAL:
        return
    _last_cache_cleanup = now
    
    before = len(_memory_cache)
    expired_keys = [
        k for k, ttl in _memory_cache_ttl.items()
        if now >= ttl
    ]
    for k in expired_keys:
        _memory_cache.pop(k, None)
        _memory_cache_ttl.pop(k, None)
    
    after = len(_memory_cache)
    if before != after:
        logger.debug("Cache cleanup: %d -> %d entries", before, after)


def get_cache(key: str) -> Optional[dict]:
    """Get value from cache (Redis or in-memory)"""
    global _redis_client
    
    # Periodic cleanup
    _cleanup_expired_cache()
    
    # Try Redis first
    if _redis_client is None:
        _redis_client = _get_redis()
    
    if _redis_client:
        try:
            data = _redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            _redis_client = None  # Reset on error
            pass
    
    # Fallback to in-memory
    if key in _memory_cache:
        if time.time() < _memory_cache_ttl.get(key, 0):
            return _memory_cache[key]
        else:
            del _memory_cache[key]
            del _memory_cache_ttl[key]
    
    return None


def set_cache(key: str, value: dict, ttl: int = 300):
    """Set value in cache (Redis or in-memory)"""
    global _redis_client
    
    # Try Redis first
    if _redis_client is None:
        _redis_client = _get_redis()
    
    if _redis_client:
        try:
            _redis_client.setex(key, ttl, json.dumps(value))
            return
        except Exception:
            _redis_client = None  # Reset on error
            pass
    
    # Fallback to in-memory
    _memory_cache[key] = value
    _memory_cache_ttl[key] = time.time() + ttl


def cache_key(*args) -> str:
    """Generate cache key from arguments"""
    raw = json.dumps(args, sort_keys=True, default=str)
    return hashlib.md5(raw.encode()).hexdigest()


def cached(ttl: int = 300):
    """Decorator for caching async function results"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{cache_key(*args, *kwargs)}"
            
            # Check cache
            result = get_cache(key)
            if result is not None:
                return result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache (only if no error)
            if result and not result.get("error"):
                set_cache(key, result, ttl)
            
            return result
        return wrapper
    return decorator


def get_cache_stats() -> dict:
    """Get cache statistics for monitoring"""
    return {
        "memory_entries": len(_memory_cache),
        "redis_connected": _redis_client is not None,
    }