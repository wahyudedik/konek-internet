"""SSL History service - Riwayat SSL certificate menggunakan crt.sh (CT Logs)"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from app.utils.cache import cached

try:
    import httpx
except ImportError:
    httpx = None


@cached(ttl=3600)
async def get_ssl_history(domain: str) -> Dict[str, Any]:
    """
    SSL History - Lihat riwayat SSL certificate dari Certificate Transparency logs.
    Menggunakan crt.sh API untuk mendapatkan semua sertifikat yang pernah diterbitkan
    untuk domain ini.
    """
    if httpx is None:
        return {"domain": domain, "certificates": [], "error": "httpx tidak terinstall"}

    try:
        # crt.sh sering lambat, gunakan timeout lebih pendek
        async with httpx.AsyncClient(
            verify=False,
            timeout=httpx.Timeout(connect=5, read=15, write=5, pool=5),
        ) as client:
            # Query crt.sh API
            url = f"https://crt.sh/?q={domain}&output=json"
            response = await client.get(url)

            if response.status_code != 200:
                return {
                    "domain": domain,
                    "certificates": [],
                    "error": f"crt.sh returned status {response.status_code}",
                }

            data = response.json()

            if not data:
                return {
                    "domain": domain,
                    "certificates": [],
                    "summary": {
                        "total_certs": 0,
                        "unique_issuers": 0,
                        "date_range": None,
                    },
                    "error": None,
                }

            # Process certificates
            certificates = []
            seen_ids = set()

            for cert in data:
                cert_id = cert.get("id")
                if cert_id in seen_ids:
                    continue
                seen_ids.add(cert_id)

                # Parse dates
                not_before = cert.get("not_before", "")
                not_after = cert.get("not_after", "")

                # Get issuer name
                issuer_name = cert.get("issuer_name", "Unknown")

                # Get common name and name values
                common_name = cert.get("common_name", "")
                name_values = cert.get("name_value", "")
                if isinstance(name_values, str):
                    name_values = [nv.strip() for nv in name_values.split("\n") if nv.strip()]

                certificates.append({
                    "id": cert_id,
                    "issuer": issuer_name,
                    "common_name": common_name,
                    "name_values": name_values if isinstance(name_values, list) else [name_values],
                    "not_before": not_before,
                    "not_after": not_after,
                    "serial_number": cert.get("serial_number", ""),
                    "entry_timestamp": cert.get("entry_timestamp", ""),
                    "not_before_timestamp": cert.get("not_before_timestamp", ""),
                    "not_after_timestamp": cert.get("not_after_timestamp", ""),
                })

            # Sort by not_before (newest first)
            certificates.sort(key=lambda x: x.get("not_before", ""), reverse=True)

            # Calculate summary
            issuers = set()
            dates = []
            for cert in certificates:
                issuers.add(cert["issuer"])
                if cert.get("not_before"):
                    dates.append(cert["not_before"])

            date_range = None
            if dates:
                date_range = {
                    "earliest": min(dates),
                    "latest": max(dates),
                }

            # Check current certificate validity
            current_cert = certificates[0] if certificates else None
            is_currently_valid = False
            if current_cert and current_cert.get("not_after"):
                from datetime import datetime
                try:
                    not_after = datetime.strptime(current_cert["not_after"], "%Y-%m-%dT%H:%M:%S")
                    is_currently_valid = not_after > datetime.now()
                except (ValueError, TypeError):
                    pass

            return {
                "domain": domain,
                "certificates": certificates,
                "total_found": len(certificates),
                "summary": {
                    "total_certs": len(certificates),
                    "unique_issuers": len(issuers),
                    "issuers": list(issuers),
                    "date_range": date_range,
                    "current_cert_valid": is_currently_valid,
                    "latest_issuer": certificates[0]["issuer"] if certificates else None,
                },
                "error": None,
            }

    except httpx.ConnectError:
        return {
            "domain": domain,
            "certificates": [],
            "error": "Tidak dapat terhubung ke crt.sh",
        }
    except httpx.TimeoutException:
        return {
            "domain": domain,
            "certificates": [],
            "error": "Timeout saat mengakses crt.sh",
        }
    except json.JSONDecodeError:
        return {
            "domain": domain,
            "certificates": [],
            "error": "Response dari crt.sh tidak valid",
        }
    except Exception as e:
        return {
            "domain": domain,
            "certificates": [],
            "error": f"Error: {str(e)}",
        }


@cached(ttl=3600)
async def get_cert_details(domain: str, cert_id: int) -> Dict[str, Any]:
    """
    SSL History - Detail sertifikat spesifik dari crt.sh.
    """
    if httpx is None:
        return {"error": "httpx tidak terinstall"}

    try:
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            url = f"https://crt.sh/?d={cert_id}"
            response = await client.get(url)

            if response.status_code == 200:
                # crt.sh returns HTML for individual cert pages
                # For simplicity, return the raw data
                return {
                    "cert_id": cert_id,
                    "url": url,
                    "detail_url": f"https://crt.sh/?d={cert_id}",
                    "error": None,
                }
            else:
                return {"cert_id": cert_id, "error": f"Status {response.status_code}"}

    except Exception as e:
        return {"cert_id": cert_id, "error": str(e)}
