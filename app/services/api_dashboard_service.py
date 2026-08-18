"""API Dashboard service - Usage stats dan rate limit info untuk API consumers"""
import time
from typing import Dict, Any, List
from app.utils.rate_limit import get_remaining_requests, MAX_REQUESTS, WINDOW_SIZE


# API endpoint registry - semua endpoints yang tersedia
API_ENDPOINTS = [
    # DNS Tools
    {"method": "GET", "path": "/api/v1/dns/{domain}", "category": "DNS", "description": "DNS Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/reverse", "category": "DNS", "description": "Reverse DNS Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/mx", "category": "DNS", "description": "MX Record Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/txt", "category": "DNS", "description": "TXT Record Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/cname", "category": "DNS", "description": "CNAME Record Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/spf", "category": "DNS", "description": "SPF Record Check", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/dmarc", "category": "DNS", "description": "DMARC Record Check", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/propagation", "category": "DNS", "description": "DNS Propagation Check", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/dns/{domain}/history", "category": "DNS", "description": "DNS History (Multi-Resolver)", "params": "domain (string), record_type (string, optional)"},
    # Domain Tools
    {"method": "GET", "path": "/api/v1/whois/{domain}", "category": "Domain", "description": "WHOIS Lookup", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/domain/{domain}/expiry", "category": "Domain", "description": "Domain Expiry Check", "params": "domain (string)"},
    # SSL Tools
    {"method": "GET", "path": "/api/v1/ssl/{domain}", "category": "SSL", "description": "SSL Certificate Check", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/ssl/{domain}/expiry", "category": "SSL", "description": "SSL Expiry Check", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/ssl/{domain}/cert-history", "category": "SSL", "description": "SSL Certificate History (CT Logs)", "params": "domain (string)"},
    # Website Tools
    {"method": "GET", "path": "/api/v1/ping/{host}", "category": "Website", "description": "Ping Checker", "params": "host (string)"},
    {"method": "GET", "path": "/api/v1/http-status/{url}", "category": "Website", "description": "HTTP Status Check", "params": "url (string)"},
    {"method": "GET", "path": "/api/v1/redirect/{url}", "category": "Website", "description": "Redirect Chain Check", "params": "url (string)"},
    {"method": "GET", "path": "/api/v1/headers/{url}", "category": "Website", "description": "HTTP Headers Check", "params": "url (string)"},
    {"method": "GET", "path": "/api/v1/ua", "category": "Website", "description": "User-Agent Detection", "params": "-"},
    {"method": "GET", "path": "/api/v1/ua/{encoded_ua:path}", "category": "Website", "description": "User-Agent Parse", "params": "encoded_ua (string)"},
    {"method": "GET", "path": "/api/v1/cdn/{domain}/detect", "category": "Website", "description": "CDN Detection", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/traceroute/{host}", "category": "Website", "description": "Traceroute", "params": "host (string)"},
    {"method": "GET", "path": "/api/v1/tech/{domain}/detect", "category": "Website", "description": "Technology Detection", "params": "domain (string)"},
    {"method": "GET", "path": "/api/v1/speed/{domain}", "category": "Website", "description": "Website Speed Test", "params": "domain (string)"},
    # IP Tools
    {"method": "GET", "path": "/api/v1/ip/{ip}", "category": "IP", "description": "IP Lookup", "params": "ip (string)"},
    {"method": "GET", "path": "/api/v1/ip/{ip}/asn", "category": "IP", "description": "ASN Lookup", "params": "ip (string)"},
    {"method": "GET", "path": "/api/v1/ip/{ip}/blacklist", "category": "IP", "description": "Blacklist Check", "params": "ip (string)"},
    {"method": "GET", "path": "/api/v1/ip/me", "category": "IP", "description": "My IP Address", "params": "-"},
    {"method": "GET", "path": "/api/v1/email/{email}/validate", "category": "IP", "description": "Email Validation", "params": "email (string)"},
    {"method": "GET", "path": "/api/v1/port/{host}", "category": "IP", "description": "Port Scanner", "params": "host (string), ports (string, optional)"},
    # Dynamic DNS
    {"method": "GET", "path": "/api/v1/ddns/records", "category": "Dynamic DNS", "description": "List DDNS Records", "params": "- (auth required)"},
    {"method": "POST", "path": "/api/v1/ddns/records", "category": "Dynamic DNS", "description": "Create DDNS Record", "params": "hostname, domain, record_type, ttl, provider (auth required)"},
    {"method": "GET", "path": "/api/v1/ddns/records/{id}", "category": "Dynamic DNS", "description": "Get DDNS Record", "params": "id (int, auth required)"},
    {"method": "PUT", "path": "/api/v1/ddns/records/{id}", "category": "Dynamic DNS", "description": "Update DDNS Record", "params": "id (int, auth required)"},
    {"method": "DELETE", "path": "/api/v1/ddns/records/{id}", "category": "Dynamic DNS", "description": "Delete DDNS Record", "params": "id (int, auth required)"},
    {"method": "GET", "path": "/api/v1/ddns/update", "category": "Dynamic DNS", "description": "Update IP via Token", "params": "token (string), ip (string)"},
]


def get_api_dashboard(ip: str) -> Dict[str, Any]:
    """
    API Dashboard - Statistik usage dan info rate limit.
    """
    remaining = get_remaining_requests(ip)
    
    # Group endpoints by category
    categories = {}
    for ep in API_ENDPOINTS:
        cat = ep["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ep)
    
    # Category stats
    category_stats = {}
    for cat, endpoints in categories.items():
        category_stats[cat] = {
            "count": len(endpoints),
            "endpoints": endpoints,
        }
    
    return {
        "rate_limit": {
            "max_requests": MAX_REQUESTS,
            "window_seconds": WINDOW_SIZE,
            "remaining": remaining,
            "description": f"{MAX_REQUESTS} requests per {WINDOW_SIZE} seconds per IP",
        },
        "total_endpoints": len(API_ENDPOINTS),
        "categories": category_stats,
        "base_url": "https://konektivitas.com",
        "api_prefix": "/api/v1",
        "authentication": {
            "required": False,
            "description": "Public API - Tidak perlu API key untuk public tools",
            "future": "API key (kn_ prefix) diperlukan untuk premium features",
        },
        "rate_limit_headers": {
            "X-RateLimit-Limit": f"Jumlah maksimal request ({MAX_REQUESTS})",
            "X-RateLimit-Remaining": f"Sisa request yang tersisa",
            "X-RateLimit-Reset": f"Waktu reset (epoch timestamp)",
        },
        "example_requests": [
            {
                "tool": "DNS Lookup",
                "url": "/api/v1/dns/google.com",
                "method": "GET",
            },
            {
                "tool": "WHOIS Lookup",
                "url": "/api/v1/whois/google.com",
                "method": "GET",
            },
            {
                "tool": "SSL Check",
                "url": "/api/v1/ssl/google.com",
                "method": "GET",
            },
            {
                "tool": "My IP",
                "url": "/api/v1/ip/me",
                "method": "GET",
            },
        ],
    }
