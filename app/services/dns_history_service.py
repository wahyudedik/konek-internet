"""DNS History service - Riwayat DNS record menggunakan multiple nameserver"""
import asyncio
import dns.resolver
from typing import Dict, Any, List
from app.utils.cache import cached

# Public DNS resolvers untuk cross-check
PUBLIC_DNS = {
    "Google (8.8.8.8)": "8.8.8.8",
    "Google (8.8.4.4)": "8.8.4.4",
    "Cloudflare (1.1.1.1)": "1.1.1.1",
    "Cloudflare (1.0.0.1)": "1.0.0.1",
    "OpenDNS (208.67.222.222)": "208.67.222.222",
    "Quad9 (9.9.9.9)": "9.9.9.9",
}


@cached(ttl=300)
async def get_dns_history(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """
    DNS History - Periksa DNS records dari multiple nameserver.
    Membandingkan hasil dari berbagai resolver untuk mendeteksi
    perbedaan propagasi DNS.
    """
    results = {}
    errors = []

    async def query_ns(name: str, ns_ip: str) -> tuple:
        """Query single nameserver"""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [ns_ip]
            resolver.lifetime = 5

            def _resolve():
                try:
                    answers = resolver.resolve(domain, record_type)
                    records = []
                    for rdata in answers:
                        records.append(str(rdata))
                    return {
                        "records": sorted(records),
                        "ttl": answers.rrset.ttl if answers.rrset else None,
                        "error": None,
                    }
                except dns.resolver.NoAnswer:
                    return {"records": [], "ttl": None, "error": "No records found"}
                except dns.resolver.NXDOMAIN:
                    return {"records": [], "ttl": None, "error": "Domain not found"}
                except dns.resolver.NoNameservers:
                    return {"records": [], "ttl": None, "error": "Nameserver error"}
                except Exception as e:
                    return {"records": [], "ttl": None, "error": str(e)}

            result = await asyncio.to_thread(_resolve)
            return (name, result)
        except Exception as e:
            return (name, {"records": [], "ttl": None, "error": str(e)})

    # Query all nameservers in parallel
    tasks = [query_ns(name, ip) for name, ip in PUBLIC_DNS.items()]
    completed = await asyncio.gather(*tasks, return_exceptions=True)

    for result in completed:
        if isinstance(result, Exception):
            errors.append(str(result))
            continue
        name, data = result
        results[name] = data

    # Analyze consistency
    all_records = {}
    for ns_name, ns_data in results.items():
        if ns_data.get("records"):
            for record in ns_data["records"]:
                if record not in all_records:
                    all_records[record] = []
                all_records[record].append(ns_name)

    # Determine consistency
    total_ns = len(results)
    successful_ns = sum(1 for r in results.values() if r.get("records"))

    if successful_ns == 0:
        consistency = "TIDAK_DITEMUKAN"
        consistency_desc = "Record tidak ditemukan di nameserver manapun"
    elif len(all_records) == 1:
        consistency = "KONSISTEN"
        consistency_desc = "Semua nameserver memberikan hasil yang sama"
    elif len(all_records) <= 3:
        consistency = "SEBAGIAN_BEDA"
        consistency_desc = f"Beberapa nameserver memberikan hasil berbeda (mungkin belum propagate)"
    else:
        consistency = "BANYAK_BEDA"
        consistency_desc = "Banyak perbedaan antar nameserver (propagasi sedang berlangsung)"

    # Get TTL info
    ttls = [r.get("ttl") for r in results.values() if r.get("ttl") is not None]
    avg_ttl = round(sum(ttls) / len(ttls)) if ttls else None

    return {
        "domain": domain,
        "record_type": record_type,
        "results": results,
        "summary": {
            "total_nameservers": total_ns,
            "successful_queries": successful_ns,
            "unique_records": len(all_records),
            "consistency": consistency,
            "consistency_description": consistency_desc,
            "average_ttl": avg_ttl,
            "all_records": all_records,
        },
        "record_types_available": [
            "A", "AAAA", "MX", "TXT", "CNAME", "NS", "SOA", "SRV", "CAA"
        ],
        "error": "; ".join(errors) if errors else None,
    }


@cached(ttl=300)
async def get_all_record_types(domain: str) -> Dict[str, Any]:
    """
    DNS History - Cek semua jenis record untuk domain.
    Mengembalikan semua record dari resolver default.
    """
    record_types = ["A", "AAAA", "MX", "TXT", "CNAME", "NS", "SOA", "SRV", "CAA"]
    results = {}

    for rtype in record_types:
        try:
            def _resolve(rt):
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.lifetime = 5
                    answers = resolver.resolve(domain, rt)
                    records = []
                    for rdata in answers:
                        records.append(str(rdata))
                    return {"records": records, "ttl": answers.rrset.ttl if answers.rrset else None}
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                    return None
                except Exception:
                    return None

            result = await asyncio.to_thread(_resolve, rtype)
            if result and result.get("records"):
                results[rtype] = result
        except Exception:
            pass

    return {
        "domain": domain,
        "records": results,
        "total_types_found": len(results),
    }
