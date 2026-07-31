import dns.resolver
from typing import Dict, List, Any, Optional
from app.utils.cache import cached


@cached(ttl=300)
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


@cached(ttl=600)
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


async def propagation_check(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """DNS Propagation Checker - Cek DNS dari multiple nameserver global"""
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
    
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        
        for name, ns_ip in nameservers.items():
            try:
                resolver.nameservers = [ns_ip]
                answers = resolver.resolve(domain, record_type)
                records = [str(r) for r in answers]
                results["results"][name] = {
                    "ip": ns_ip,
                    "records": records,
                    "status": "ok"
                }
            except dns.resolver.NXDOMAIN:
                results["results"][name] = {
                    "ip": ns_ip,
                    "records": [],
                    "status": "nxdomain"
                }
            except dns.resolver.NoAnswer:
                results["results"][name] = {
                    "ip": ns_ip,
                    "records": [],
                    "status": "noanswer"
                }
            except Exception as e:
                results["results"][name] = {
                    "ip": ns_ip,
                    "records": [],
                    "status": f"error: {str(e)}"
                }
        
        # Collect unique records
        all_records = set()
        for data in results["results"].values():
            for r in data.get("records", []):
                all_records.add(r)
        results["unique_records"] = list(all_records)
        
    except Exception as e:
        results["error"] = str(e)
    
    return results