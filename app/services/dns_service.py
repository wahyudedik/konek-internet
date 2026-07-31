import dns.resolver
from typing import Dict, List, Any, Optional


async def lookup_dns(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """DNS Lookup - Query DNS records untuk domain"""
    results = {
        "domain": domain,
        "record_type": record_type,
        "records": [],
        "error": None
    }
    
    try:
        answers = dns.resolver.resolve(domain, record_type)
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


async def reverse_dns(ip_address: str) -> Dict[str, Any]:
    """Reverse DNS - Lookup IP ke domain"""
    results = {
        "ip": ip_address,
        "domains": [],
        "error": None
    }
    
    try:
        hostname = dns.reversename.from_address(ip_address)
        answers = dns.resolver.resolve(hostname, "PTR")
        for rdata in answers:
            results["domains"].append(str(rdata))
    except Exception as e:
        results["error"] = str(e)
    
    return results


async def lookup_mx(domain: str) -> Dict[str, Any]:
    """MX Lookup - Cek mail exchange records"""
    return await lookup_dns(domain, "MX")


async def lookup_txt(domain: str) -> Dict[str, Any]:
    """TXT Lookup - Cek TXT records"""
    return await lookup_dns(domain, "TXT")


async def lookup_cname(domain: str) -> Dict[str, Any]:
    """CNAME Lookup - Cek canonical name records"""
    return await lookup_dns(domain, "CNAME")


async def check_spf(domain: str) -> Dict[str, Any]:
    """SPF Checker - Validasi SPF records"""
    results = await lookup_dns(domain, "TXT")
    
    # Filter SPF records
    spf_records = [r for r in results["records"] if "v=spf1" in r]
    results["spf_records"] = spf_records
    results["has_spf"] = len(spf_records) > 0
    
    return results


async def check_dmarc(domain: str) -> Dict[str, Any]:
    """DMARC Checker - Validasi DMARC policies"""
    dmarc_domain = f"_dmarc.{domain}"
    results = await lookup_dns(dmarc_domain, "TXT")
    results["dmarc_domain"] = dmarc_domain
    results["has_dmarc"] = len(results["records"]) > 0
    
    return results