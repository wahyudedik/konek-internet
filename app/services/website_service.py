"""Website service - Business logic untuk ping, HTTP status, redirect, headers"""
import httpx
import asyncio
import socket
import time
from typing import Dict, Any, Optional
from app.utils.cache import cached


# Shared HTTP client for connection pooling
_http_client: httpx.AsyncClient = None

async def _get_client(**kwargs) -> httpx.AsyncClient:
    """Get or create shared HTTP client with connection pooling"""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            verify=False,
            follow_redirects=True,
            timeout=10,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    return _http_client

async def _fetch_with_fallback(url: str, method: str = "GET", **kwargs):
    """Try HTTPS first, fallback to HTTP"""
    # Normalisasi URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    client = await _get_client()

    # Coba HTTPS dulu
    https_url = url if url.startswith('https://') else url.replace('http://', 'https://', 1)
    try:
        response = await client.request(method, https_url, **kwargs)
        return response, https_url
    except Exception:
        pass

    # Fallback ke HTTP
    http_url = https_url.replace('https://', 'http://', 1)
    response = await client.request(method, http_url, **kwargs)
    return response, http_url


def _ping_sync(host: str) -> Dict[str, Any]:
    """Synchronous ping using socket"""
    results = {
        "domain": host,
        "reachable": False,
        "response_time_ms": None,
        "status_code": None,
        "error": None
    }

    try:
        start = time.time()
        sock = socket.create_connection((host, 443), timeout=5)
        sock.close()
        elapsed = (time.time() - start) * 1000
        results["reachable"] = True
        results["response_time_ms"] = round(elapsed, 2)
    except socket.timeout:
        results["error"] = "Timeout"
    except socket.gaierror:
        results["error"] = "Domain tidak dapat diresolve"
    except ConnectionRefusedError:
        results["error"] = "Koneksi ditolak"
    except Exception as e:
        results["error"] = str(e)

    return results


@cached(ttl=60)
async def ping_host(host: str) -> Dict[str, Any]:
    """Ping Checker - Uji konektivitas ke server via HTTP(S)"""
    results = {
        "domain": host,
        "reachable": False,
        "response_time_ms": None,
        "status_code": None,
        "error": None
    }

    try:
        response, used_url = await _fetch_with_fallback(host)
        results["reachable"] = True
        results["status_code"] = response.status_code
        results["response_time_ms"] = response.elapsed.total_seconds() * 1000
        results["url_used"] = used_url
    except httpx.TimeoutException:
        results["error"] = "Timeout"
    except httpx.ConnectError:
        results["error"] = "Koneksi gagal"
    except Exception as e:
        results["error"] = str(e)

    return results


@cached(ttl=120)
async def check_http_status(url: str) -> Dict[str, Any]:
    """HTTP Status Checker - Cek status HTTP response"""
    # Normalisasi URL untuk domain input
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    results = {
        "domain": url,
        "status_code": None,
        "status_text": None,
        "error": None
    }

    try:
        response, used_url = await _fetch_with_fallback(url)
        results["status_code"] = response.status_code
        results["status_text"] = response.reason_phrase
        results["url_used"] = used_url
    except Exception as e:
        results["error"] = str(e)

    return results


@cached(ttl=120)
async def check_redirects(url: str) -> Dict[str, Any]:
    """Redirect Checker - Lacak redirect chains"""
    # Normalisasi URL untuk domain input
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    results = {
        "domain": url,
        "redirects": [],
        "final_url": None,
        "error": None
    }

    try:
        # Manual redirect tracking
        https_url = url if url.startswith('https://') else url.replace('http://', 'https://', 1)
        current_url = https_url
        max_redirects = 10
        redirect_chain = []

        for _ in range(max_redirects):
            try:
                async with httpx.AsyncClient(follow_redirects=False, timeout=10) as client:
                    response = await client.get(current_url)
            except Exception:
                # Fallback ke HTTP
                current_url = current_url.replace('https://', 'http://', 1)
                try:
                    async with httpx.AsyncClient(follow_redirects=False, timeout=10) as client:
                        response = await client.get(current_url)
                except Exception as e:
                    raise e

            if response.status_code in (301, 302, 303, 307, 308):
                redirect_chain.append({
                    "url": str(response.url),
                    "status_code": response.status_code
                })
                location = response.headers.get("location", "")
                if not location:
                    break
                # Handle relative redirect
                if location.startswith("/"):
                    from urllib.parse import urlparse
                    parsed = urlparse(str(response.url))
                    location = f"{parsed.scheme}://{parsed.netloc}{location}"
                current_url = location
            else:
                break

        results["redirects"] = redirect_chain
        results["final_url"] = current_url
        results["final_status"] = response.status_code
    except Exception as e:
        results["error"] = str(e)

    return results


@cached(ttl=120)
async def check_headers(url: str) -> Dict[str, Any]:
    """Header Checker - Analisis HTTP headers dengan HTTP version detection"""
    # Normalisasi URL untuk domain input
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    results = {
        "domain": url,
        "headers": {},
        "http_version": None,
        "http_version_supported": {},
        "error": None
    }

    try:
        response, used_url = await _fetch_with_fallback(url)
        results["headers"] = dict(response.headers)
        results["url_used"] = used_url
        
        # HTTP Version Detection
        http_version = "HTTP/1.1"  # default
        if hasattr(response, 'http_version'):
            http_version = response.http_version
        elif hasattr(response, 'version'):
            version_map = {10: "HTTP/1.0", 11: "HTTP/1.1", 20: "HTTP/2", 30: "HTTP/3"}
            http_version = version_map.get(response.version, f"HTTP/{response.version/10}")
        
        results["http_version"] = http_version
        results["http_version_supported"] = {
            "http10": True,
            "http11": True,
            "http2": "HTTP/2" in http_version,
            "http3": "HTTP/3" in http_version,
        }
    except Exception as e:
        results["error"] = str(e)

    return results
