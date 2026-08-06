import httpx
import logging
from typing import Dict, Any
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.ip")


@cached(ttl=3600)
async def lookup_ip(ip_address: str) -> Dict[str, Any]:
    """IP Lookup - Informasi IP address"""
    results = {
        "ip": ip_address,
        "city": None,
        "region": None,
        "country": None,
        "timezone": None,
        "isp": None,
        "org": None,
        "as": None,
        "error": None
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{ip_address}", timeout=10)
            data = response.json()
            
            if data.get("status") == "success":
                results["city"] = data.get("city")
                results["region"] = data.get("regionName")
                results["country"] = data.get("country")
                results["timezone"] = data.get("timezone")
                results["isp"] = data.get("isp")
                results["org"] = data.get("org")
                results["as"] = data.get("as")
            else:
                results["error"] = data.get("message", "Gagal melakukan lookup")
    except Exception as e:
        results["error"] = str(e)
    
    return results


@cached(ttl=3600)
async def lookup_asn(ip_address: str) -> Dict[str, Any]:
    """ASN Lookup - Cek Autonomous System Number"""
    results = await lookup_ip(ip_address)
    
    if results.get("as"):
        asn_parts = results["as"].split(" ", 1)
        results["asn"] = asn_parts[0] if asn_parts else None
        results["asn_organization"] = asn_parts[1] if len(asn_parts) > 1 else None
    
    return results


@cached(ttl=600)
async def check_blacklist(ip_address: str) -> Dict[str, Any]:
    """Blacklist Checker - Cek apakah IP ada di blacklist"""
    import asyncio
    
    results = {
        "ip": ip_address,
        "blacklisted": False,
        "blacklists": [],
        "error": None
    }
    
    blacklist_servers = [
        "zen.spamhaus.org",
        "bl.spamcop.net",
        "b.barracudacentral.org",
        "dnsbl-1.uceprotect.net",
        "spam.dnsbl.sorbs.net"
    ]
    
    def _check_sync():
        """Blocking DNS check wrapped for async safety"""
        import dns.resolver
        
        # Blacklist DNSBL hanya mendukung IPv4
        parts = ip_address.split(".")
        if len(parts) != 4:
            return []  # IPv6 tidak didukung oleh DNSBL
        
        reversed_ip = ".".join(reversed(parts))
        found = []
        for bl_server in blacklist_servers:
            try:
                query = f"{reversed_ip}.{bl_server}"
                dns.resolver.resolve(query, "A", lifetime=5)
                found.append(bl_server)
            except dns.resolver.NXDOMAIN:
                pass
            except (dns.resolver.NoAnswer, dns.resolver.Timeout,
                    dns.exception.DNSException):
                pass
            except Exception:
                pass
        return found
    
    try:
        found = await asyncio.to_thread(_check_sync)
        if found:
            results["blacklists"] = found
            results["blacklisted"] = True
    except Exception as e:
        results["error"] = str(e)
    
    return results