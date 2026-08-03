"""CDN Detection Service - Deteksi provider CDN menggunakan DNS CNAME + HTTP Headers"""
import asyncio
import dns.resolver
import logging
from typing import Dict, Any, List, Optional
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.cdn")

# ============ CDN SIGNATURES ============

# CNAME patterns -> CDN provider
_CNAME_PATTERNS = {
    "cloudflare.com": {
        "name": "Cloudflare",
        "slug": "cloudflare",
        "url": "https://www.cloudflare.com",
        "description": "CDN & DDoS protection terbesar di dunia",
    },
    "cloudfront.net": {
        "name": "AWS CloudFront",
        "slug": "cloudfront",
        "url": "https://aws.amazon.com/cloudfront/",
        "description": "CDN dari Amazon Web Services",
    },
    "akamaiedge.net": {
        "name": "Akamai",
        "slug": "akamai",
        "url": "https://www.akamai.com",
        "description": "CDN terbesar berdasarkan jumlah server",
    },
    "edgekey.net": {
        "name": "Akamai",
        "slug": "akamai",
        "url": "https://www.akamai.com",
        "description": "CDN terbesar berdasarkan jumlah server",
    },
    "fastly.net": {
        "name": "Fastly",
        "slug": "fastly",
        "url": "https://www.fastly.com",
        "description": "Edge cloud platform untuk real-time apps",
    },
    "hwcdn.net": {
        "name": "StackPath",
        "slug": "stackpath",
        "url": "https://www.stackpath.com",
        "description": "Edge computing & CDN platform",
    },
    "azureedge.net": {
        "name": "Azure CDN",
        "slug": "azure",
        "url": "https://azure.microsoft.com/en-us/services/cdn/",
        "description": "CDN dari Microsoft Azure",
    },
    "azurefd.net": {
        "name": "Azure Front Door",
        "slug": "azure",
        "url": "https://azure.microsoft.com/en-us/services/frontdoor/",
        "description": "Global CDN & load balancer dari Azure",
    },
    "cdn77.org": {
        "name": "CDN77",
        "slug": "cdn77",
        "url": "https://www.cdn77.com",
        "description": "CDN provider dengan POP di 6 benua",
    },
    "keycdn.com": {
        "name": "KeyCDN",
        "slug": "keycdn",
        "url": "https://www.keycdn.com",
        "description": "High performance CDN",
    },
    "incapsula.com": {
        "name": "Imperva",
        "slug": "imperva",
        "url": "https://www.imperva.com",
        "description": "CDN & web security (sebelumnya Incapsula)",
    },
    "internap.com": {
        "name": "Internap",
        "slug": "internap",
        "url": "https://www.internap.com",
        "description": "Managed hosting & CDN",
    },
    "edgecastcdn.net": {
        "name": "Verizon Digital Media",
        "slug": "verizon",
        "url": "https://www.verizondigitalmedia.com",
        "description": "CDN dari Verizon",
    },
    "cdn.cloudflare.net": {
        "name": "Cloudflare",
        "slug": "cloudflare",
        "url": "https://www.cloudflare.com",
        "description": "CDN & DDoS protection terbesar di dunia",
    },
    "kxcdn.com": {
        "name": "KeyCDN",
        "slug": "keycdn",
        "url": "https://www.keycdn.com",
        "description": "High performance CDN",
    },
    "stackpathdns.com": {
        "name": "StackPath",
        "slug": "stackpath",
        "url": "https://www.stackpath.com",
        "description": "Edge computing & CDN platform",
    },
    "librespeedcdn.net": {
        "name": "LibreSpeed CDN",
        "slug": "librespeed",
        "url": "#",
        "description": "Open source CDN",
    },
    "gslb.vdacdn.com": {
        "name": "CDNetworks",
        "slug": "cdnetworks",
        "url": "https://www.cdnetworks.com",
        "description": "CDN provider di Asia",
    },
}

# HTTP header patterns -> CDN provider
_HEADER_PATTERNS = {
    "cf-ray": {
        "name": "Cloudflare",
        "slug": "cloudflare",
        "url": "https://www.cloudflare.com",
        "description": "CDN & DDoS protection terbesar di dunia",
    },
    "cf-cache-status": {
        "name": "Cloudflare",
        "slug": "cloudflare",
        "url": "https://www.cloudflare.com",
        "description": "CDN & DDoS protection terbesar di dunia",
    },
    "x-amz-cf-id": {
        "name": "AWS CloudFront",
        "slug": "cloudfront",
        "url": "https://aws.amazon.com/cloudfront/",
        "description": "CDN dari Amazon Web Services",
    },
    "x-amz-cf-pop": {
        "name": "AWS CloudFront",
        "slug": "cloudfront",
        "url": "https://aws.amazon.com/cloudfront/",
        "description": "CDN dari Amazon Web Services",
    },
    "x-fastly-request-id": {
        "name": "Fastly",
        "slug": "fastly",
        "url": "https://www.fastly.com",
        "description": "Edge cloud platform untuk real-time apps",
    },
    "x-akamai-transformed": {
        "name": "Akamai",
        "slug": "akamai",
        "url": "https://www.akamai.com",
        "description": "CDN terbesar berdasarkan jumlah server",
    },
    "x-akamai-request-id": {
        "name": "Akamai",
        "slug": "akamai",
        "url": "https://www.akamai.com",
        "description": "CDN terbesar berdasarkan jumlah server",
    },
    "x-azure-ref": {
        "name": "Azure CDN",
        "slug": "azure",
        "url": "https://azure.microsoft.com/en-us/services/cdn/",
        "description": "CDN dari Microsoft Azure",
    },
    "x-msedge-ref": {
        "name": "Azure Front Door",
        "slug": "azure",
        "url": "https://azure.microsoft.com/en-us/services/frontdoor/",
        "description": "Global CDN & load balancer dari Azure",
    },
    "x-cdn": {
        "name": "CDN Provider",
        "slug": "cdn",
        "url": "#",
        "description": "Generic CDN detected via x-cdn header",
    },
    "x-cache": {
        "name": "Cache Server",
        "slug": "cache",
        "url": "#",
        "description": "Cache server detected (mungkin CDN)",
    },
    "x-hw": {
        "name": "StackPath/Highwinds",
        "slug": "stackpath",
        "url": "https://www.stackpath.com",
        "description": "Edge computing & CDN platform",
    },
    "via": {
        "name": "Proxy/CDN",
        "slug": "proxy",
        "url": "#",
        "description": "Proxy atau CDN terdeteksi via Via header",
    },
}


def _get_cname_chain(domain: str) -> Dict[str, Any]:
    """Resolve CNAME chain for a domain synchronously"""
    results = {
        "domain": domain,
        "cname_chain": [],
        "final_ips": [],
        "error": None,
    }

    current = domain
    visited = set()
    max_hops = 10

    try:
        for _ in range(max_hops):
            if current in visited:
                break
            visited.add(current)

            try:
                answers = dns.resolver.resolve(current, "CNAME")
                for rdata in answers:
                    cname_target = str(rdata).rstrip(".")
                    results["cname_chain"].append({
                        "from": current,
                        "to": cname_target,
                    })
                    current = cname_target
            except dns.resolver.NoAnswer:
                # No more CNAME, resolve A/AAAA
                break
            except dns.resolver.NXDOMAIN:
                break

        # Resolve final A/AAAA records
        try:
            a_answers = dns.resolver.resolve(current, "A")
            results["final_ips"] = [str(r) for r in a_answers]
        except Exception:
            pass

        try:
            aaaa_answers = dns.resolver.resolve(current, "AAAA")
            results["final_ips"].extend([str(r) for r in aaaa_answers])
        except Exception:
            pass

    except Exception as e:
        results["error"] = str(e)

    return results


def _detect_cdn_from_cname(cname_chain: List[Dict]) -> List[Dict[str, Any]]:
    """Detect CDN provider from CNAME chain"""
    detected = []
    seen_slugs = set()

    for entry in cname_chain:
        to_domain = entry["to"].lower()
        for pattern, info in _CNAME_PATTERNS.items():
            if pattern in to_domain and info["slug"] not in seen_slugs:
                detected.append({
                    "name": info["name"],
                    "slug": info["slug"],
                    "url": info["url"],
                    "description": info["description"],
                    "source": "CNAME",
                    "matched_pattern": pattern,
                    "matched_value": to_domain,
                })
                seen_slugs.add(info["slug"])

    return detected


def _detect_cdn_from_headers(headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Detect CDN provider from HTTP headers"""
    detected = []
    seen_slugs = set()

    for header_name, info in _HEADER_PATTERNS.items():
        # Check exact header match (case-insensitive)
        header_value = None
        for k, v in headers.items():
            if k.lower() == header_name.lower():
                header_value = v
                break

        if header_value and info["slug"] not in seen_slugs:
            detected.append({
                "name": info["name"],
                "slug": info["slug"],
                "url": info["url"],
                "description": info["description"],
                "source": "Header",
                "matched_pattern": header_name,
                "matched_value": header_value[:200] if header_value else "",
            })
            seen_slugs.add(info["slug"])

    return detected


@cached(ttl=300)
async def detect_cdn(domain: str) -> Dict[str, Any]:
    """Detect CDN provider for a domain using DNS CNAME + HTTP Headers"""
    results = {
        "domain": domain,
        "has_cdn": False,
        "cdn_providers": [],
        "cname_chain": [],
        "final_ips": [],
        "headers_analyzed": {},
        "cache_status": None,
        "error": None,
    }

    try:
        # Step 1: Resolve CNAME chain
        cname_results = await asyncio.to_thread(_get_cname_chain, domain)
        results["cname_chain"] = cname_results["cname_chain"]
        results["final_ips"] = cname_results["final_ips"]

        # Detect from CNAME
        cdn_from_cname = _detect_cdn_from_cname(cname_results["cname_chain"])

        # Step 2: Fetch HTTP headers
        import httpx
        cdn_from_headers = []
        try:
            async with httpx.AsyncClient(verify=False, follow_redirects=True, timeout=10) as client:
                https_url = f"https://{domain}"
                try:
                    response = await client.get(https_url)
                except Exception:
                    http_url = f"http://{domain}"
                    response = await client.get(http_url)

                # Store relevant headers
                relevant_headers = {}
                for k, v in response.headers.items():
                    lower_k = k.lower()
                    if lower_k in ("server", "via", "x-cache", "x-served-by",
                                   "x-powered-by", "content-type", "cf-ray",
                                   "cf-cache-status", "x-amz-cf-id", "x-amz-cf-pop",
                                   "x-fastly-request-id", "x-akamai-transformed",
                                   "x-akamai-request-id", "x-azure-ref", "x-msedge-ref",
                                   "x-cdn", "x-hw", "age", "x-varnish", "x-generator"):
                        relevant_headers[k] = v

                results["headers_analyzed"] = relevant_headers
                results["cache_status"] = relevant_headers.get("x-cache") or \
                    relevant_headers.get("cf-cache-status") or None

                cdn_from_headers = _detect_cdn_from_headers(dict(response.headers))

        except Exception as e:
            logger.warning("HTTP header fetch failed for %s: %s", domain, str(e))

        # Step 3: Merge results (deduplicate by slug)
        all_providers = {}
        for p in cdn_from_cname:
            slug = p["slug"]
            if slug not in all_providers:
                all_providers[slug] = p
            else:
                # Merge sources
                if all_providers[slug]["source"] != p["source"]:
                    all_providers[slug]["source"] = f"{all_providers[slug]['source']} + {p['source']}"

        for p in cdn_from_headers:
            slug = p["slug"]
            if slug not in all_providers:
                all_providers[slug] = p
            else:
                if all_providers[slug]["source"] != p["source"]:
                    all_providers[slug]["source"] = f"{all_providers[slug]['source']} + {p['source']}"

        # Filter out generic/proxy detections if specific CDN found
        specific_slugs = {s for s in all_providers if s not in ("cdn", "cache", "proxy")}
        if specific_slugs:
            results["cdn_providers"] = [
                p for s, p in all_providers.items() if s in specific_slugs
            ]
        else:
            results["cdn_providers"] = list(all_providers.values())

        results["has_cdn"] = len(results["cdn_providers"]) > 0

    except Exception as e:
        results["error"] = str(e)
        logger.error("CDN detection error for %s: %s", domain, str(e))

    return results
