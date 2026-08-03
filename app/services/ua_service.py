"""User-Agent Parser Service - Parse UA string tanpa library external"""
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("konektivitas.ua")

# ============ BROWSER PATTERNS ============
_BROWSERS = [
    # Order matters: more specific first
    (re.compile(r'Edge/(\d+)', re.I), "Microsoft Edge", "edge"),
    (re.compile(r'OPR/(\d+)', re.I), "Opera", "opera"),
    (re.compile(r'Opera[ /](\d+)', re.I), "Opera", "opera"),
    (re.compile(r'Edg/(\d+)', re.I), "Microsoft Edge", "edge"),
    (re.compile(r'Chrome/(\d+)', re.I), "Google Chrome", "chrome"),
    (re.compile(r'Firefox/(\d+)', re.I), "Mozilla Firefox", "firefox"),
    (re.compile(r'Version/(\d+).*Safari', re.I), "Apple Safari", "safari"),
    (re.compile(r'Safari/(\d+)', re.I), "Apple Safari", "safari"),
    (re.compile(r'Trident/7.*rv:(\d+)', re.I), "Internet Explorer", "ie"),
    (re.compile(r'MSIE (\d+)', re.I), "Internet Explorer", "ie"),
    (re.compile(r'YaBrowser/(\d+)', re.I), "Yandex Browser", "yandex"),
    (re.compile(r'Vivaldi/(\d+)', re.I), "Vivaldi", "vivaldi"),
    (re.compile(r'Brave/(\d+)', re.I), "Brave", "brave"),
    (re.compile(r'SamsungBrowser/(\d+)', re.I), "Samsung Browser", "samsung"),
]

# ============ OS PATTERNS ============
_OS_PATTERNS = [
    (re.compile(r'Windows NT 10', re.I), "Windows 10/11", "windows"),
    (re.compile(r'Windows NT 6\.3', re.I), "Windows 8.1", "windows"),
    (re.compile(r'Windows NT 6\.2', re.I), "Windows 8", "windows"),
    (re.compile(r'Windows NT 6\.1', re.I), "Windows 7", "windows"),
    (re.compile(r'Windows', re.I), "Windows", "windows"),
    (re.compile(r'iPhone OS (\d+[_.]?\d*)', re.I), "iOS", "ios"),
    (re.compile(r'iPad.*OS (\d+[_.]?\d*)', re.I), "iPadOS", "ipados"),
    (re.compile(r'Mac OS X (\d+[_.]\d+)', re.I), "macOS", "macos"),
    (re.compile(r'Macintosh', re.I), "macOS", "macos"),
    (re.compile(r'Android (\d+)', re.I), "Android", "android"),
    (re.compile(r'Linux; (?:U; )?Android', re.I), "Android", "android"),
    (re.compile(r'Ubuntu', re.I), "Linux (Ubuntu)", "linux"),
    (re.compile(r'Linux', re.I), "Linux", "linux"),
    (re.compile(r'CrOS', re.I), "Chrome OS", "chromeos"),
    (re.compile(r'BlackBerry', re.I), "BlackBerry OS", "blackberry"),
]

# ============ DEVICE PATTERNS ============
_DEVICE_PATTERNS = [
    (re.compile(r'iPhone', re.I), "Mobile", "mobile"),
    (re.compile(r'Android.*Mobile', re.I), "Mobile", "mobile"),
    (re.compile(r'Windows Phone', re.I), "Mobile", "mobile"),
    (re.compile(r'BlackBerry.*Mobile', re.I), "Mobile", "mobile"),
    (re.compile(r'iPad', re.I), "Tablet", "tablet"),
    (re.compile(r'Android(?!.*Mobile)', re.I), "Tablet", "tablet"),
    (re.compile(r'Tablet', re.I), "Tablet", "tablet"),
    (re.compile(r'Kindle', re.I), "Tablet", "tablet"),
]


def _detect_browser(ua_string: str) -> Dict[str, Any]:
    """Detect browser name and version from UA string"""
    for pattern, name, slug in _BROWSERS:
        match = pattern.search(ua_string)
        if match:
            return {
                "name": name,
                "version": match.group(1),
                "slug": slug,
            }
    return {
        "name": "Unknown Browser",
        "version": "unknown",
        "slug": "unknown",
    }


def _detect_os(ua_string: str) -> Dict[str, Any]:
    """Detect OS from UA string"""
    for pattern, name, slug in _OS_PATTERNS:
        match = pattern.search(ua_string)
        if match:
            # Try to extract version
            version = "unknown"
            if slug == "windows":
                ver_match = re.search(r'Windows NT (\d+\.\d+)', ua_string)
                if ver_match:
                    version = ver_match.group(1)
            elif slug == "android":
                ver_match = re.search(r'Android (\d+[\.\d]*)', ua_string)
                if ver_match:
                    version = ver_match.group(1)
            elif slug == "macos":
                ver_match = re.search(r'Mac OS X (\d+[_.]\d+)', ua_string)
                if ver_match:
                    version = ver_match.group(1).replace('_', '.')
            elif slug == "ios":
                ver_match = re.search(r'OS (\d+[_.]\d+)', ua_string)
                if ver_match:
                    version = ver_match.group(1).replace('_', '.')
            return {
                "name": name,
                "version": version,
                "slug": slug,
            }
    return {
        "name": "Unknown OS",
        "version": "unknown",
        "slug": "unknown",
    }


def _detect_device(ua_string: str) -> Dict[str, Any]:
    """Detect device type from UA string"""
    for pattern, name, slug in _DEVICE_PATTERNS:
        if pattern.search(ua_string):
            return {
                "type": name,
                "slug": slug,
            }
    return {
        "type": "Desktop",
        "slug": "desktop",
    }


def _parse_sync(ua_string: str) -> Dict[str, Any]:
    """Parse UA string synchronously"""
    browser = _detect_browser(ua_string)
    os_info = _detect_os(ua_string)
    device = _detect_device(ua_string)

    return {
        "user_agent": ua_string,
        "browser": browser,
        "os": os_info,
        "device": device,
        "is_bot": bool(re.search(
            r'bot|crawl|spider|slurp|mediapartners|facebookexternalhit|twitterbot|linkedinbot|whatsapp|telegram',
            ua_string, re.I
        )),
        "is_mobile": device["slug"] in ("mobile", "tablet"),
    }


async def parse_ua(ua_string: str) -> Dict[str, Any]:
    """Parse User-Agent string async"""
    import asyncio
    return await asyncio.to_thread(_parse_sync, ua_string)
