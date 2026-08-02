import asyncio
import dns.resolver
import logging
from typing import Dict, List, Any, Optional
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.dns")


@cached(ttl=300)
async def lookup_dns(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """DNS Lookup - Query DNS records untuk domain"""
    results = {
        "domain": domain,
        "record_type": record_type,
        "records": [],
        "error": None
    }
    
    def _resolve_sync():
        return dns.resolver.resolve(domain, record_type)
    
    try:
        answers = await asyncio.to_thread(_resolve_sync)
        for rdata in answers:
            results["records"].append(str(rdata))
    except dns.resolver.NXDOMAIN:
        results["error"] = "Domain tidak ditemukan"
    except dns.resolver.NoAnswer:
        results["error"] = f"Tidak ada {record_type} record untuk domain ini"
    except dns.resolver.NoNameservers:
        results["error"] = "Tidak dapat terhubung ke nameserver"
    except Exception as e:
        results["error"] = str(e)
    
    return results


@cached(ttl=600)
async def reverse_dns(ip_address: str) -> Dict[str, Any]:
    """Reverse DNS - Lookup IP ke domain"""
    results = {
        "ip": ip_address,
        "domains": [],
        "error": None
    }
    
    def _reverse_sync():
        hostname = dns.reversename.from_address(ip_address)
        answers = dns.resolver.resolve(hostname, "PTR")
        return [str(rdata) for rdata in answers]
    
    try:
        domains = await asyncio.to_thread(_reverse_sync)
        results["domains"] = domains
    except Exception as e:
        results["error"] = str(e)
    
    return results


@cached(ttl=300)
async def lookup_mx(domain: str) -> Dict[str, Any]:
    """MX Lookup - Cek mail exchange records"""
    return await _lookup_dns_raw(domain, "MX")


@cached(ttl=300)
async def lookup_txt(domain: str) -> Dict[str, Any]:
    """TXT Lookup - Cek TXT records"""
    return await _lookup_dns_raw(domain, "TXT")


@cached(ttl=300)
async def lookup_cname(domain: str) -> Dict[str, Any]:
    """CNAME Lookup - Cek canonical name records"""
    return await _lookup_dns_raw(domain, "CNAME")


@cached(ttl=300)
async def check_spf(domain: str) -> Dict[str, Any]:
    """SPF Checker - Validasi SPF records"""
    results = await _lookup_dns_raw(domain, "TXT")
    
    spf_records = [r for r in results["records"] if "v=spf1" in r]
    results["spf_records"] = spf_records
    results["has_spf"] = len(spf_records) > 0
    
    return results


@cached(ttl=300)
async def check_dmarc(domain: str) -> Dict[str, Any]:
    """DMARC Checker - Validasi DMARC policies"""
    dmarc_domain = f"_dmarc.{domain}"
    results = await _lookup_dns_raw(dmarc_domain, "TXT")
    results["dmarc_domain"] = dmarc_domain
    results["has_dmarc"] = len(results["records"]) > 0
    
    return results


async def _lookup_dns_raw(domain: str, record_type: str) -> Dict[str, Any]:
    """Internal DNS lookup tanpa caching"""
    results = {
        "domain": domain,
        "record_type": record_type,
        "records": [],
        "error": None
    }
    
    def _resolve_sync():
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    
    try:
        records = await asyncio.to_thread(_resolve_sync)
        results["records"] = records
    except dns.resolver.NXDOMAIN:
        results["error"] = "Domain tidak ditemukan"
    except dns.resolver.NoAnswer:
        results["error"] = f"Tidak ada {record_type} record untuk domain ini"
    except dns.resolver.NoNameservers:
        results["error"] = "Tidak dapat terhubung ke nameserver"
    except Exception as e:
        results["error"] = str(e)
    
    return results


@cached(ttl=60)
async def propagation_check(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """DNS Propagation Checker - Cek DNS dari multiple nameserver global (parallel)"""
    nameservers = {
        "Google (8.8.8.8)": "8.8.8.8",
        "Google (8.8.4.4)": "8.8.4.4",
        "Cloudflare (1.1.1.1)": "1.1.1.1",
        "Cloudflare (1.0.0.1)": "1.0.0.1",
        "OpenDNS (208.67.222.222)": "208.67.222.222",
        "Quad9 (9.9.9.9)": "9.9.9.9",
        "AdGuard (94.140.14.14)": "94.140.14.14",
    }
    
    results = {
        "domain": domain,
        "record_type": record_type,
        "results": {},
        "unique_records": [],
        "error": None
    }
    
    semaphore = asyncio.Semaphore(4)
    
    def _resolve_with_ns(ns_ip: str):
        r = dns.resolver.Resolver()
        r.timeout = 5
        r.lifetime = 5
        r.nameservers = [ns_ip]
        return r.resolve(domain, record_type)
    
    async def _resolve_ns(name: str, ns_ip: str) -> tuple:
        """Resolve single nameserver with semaphore limiting concurrency"""
        async with semaphore:
            try:
                answers = await asyncio.to_thread(_resolve_with_ns, ns_ip)
                records = [str(r) for r in answers]
                return name, {
                    "ip": ns_ip,
                    "records": records,
                    "status": "ok"
                }
            except dns.resolver.NXDOMAIN:
                return name, {
                    "ip": ns_ip,
                    "records": [],
                    "status": "nxdomain"
                }
            except dns.resolver.NoAnswer:
                return name, {
                    "ip": ns_ip,
                    "records": [],
                    "status": "noanswer"
                }
            except Exception as e:
                return name, {
                    "ip": ns_ip,
                    "records": [],
                    "status": f"error: {str(e)}"
                }
    
    try:
        # Query all nameservers in parallel (max 4 concurrent)
        tasks = [_resolve_ns(name, ns_ip) for name, ns_ip in nameservers.items()]
        resolved_results = await asyncio.gather(*tasks)
        
        for name, result_data in resolved_results:
            results["results"][name] = result_data
        
        # Collect unique records
        all_records = set()
        for data in results["results"].values():
            for r in data.get("records", []):
                all_records.add(r)
        results["unique_records"] = list(all_records)
        
    except Exception as e:
        results["error"] = str(e)
    
    return results