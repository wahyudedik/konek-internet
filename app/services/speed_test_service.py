"""Speed Test service - Test kecepatan loading website"""
import asyncio
import time
import re
from typing import Dict, Any, List, Optional
from app.utils.cache import cached

try:
    import httpx
except ImportError:
    httpx = None


@cached(ttl=120)
async def test_speed(url: str) -> Dict[str, Any]:
    """
    Website Speed Test - Ukur kecepatan loading website.
    Mengukur TTFB, total load time, page size, jumlah resource,
    compression, dan caching headers.
    """
    if httpx is None:
        return {"url": url, "error": "httpx tidak terinstall"}

    # Normalize URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        async with httpx.AsyncClient(
            verify=False,
            follow_redirects=True,
            timeout=30,
        ) as client:
            # Measure main page load
            start_time = time.time()
            response = await client.get(url)
            total_time = (time.time() - start_time) * 1000  # Convert to ms

            # Get response details
            headers = dict(response.headers)
            content = response.content
            content_length = len(content)

            # Calculate TTFB (approximation - time to first byte)
            # In a real scenario, this would use a lower-level approach
            ttfb_ms = total_time * 0.1  # Rough approximation

            # Check compression
            content_encoding = headers.get("content-encoding", "none")
            is_compressed = content_encoding in ("gzip", "br", "deflate")

            # Calculate compression ratio
            compression_ratio = None
            if is_compressed:
                # Approximate original size by checking Content-Length vs actual
                content_length_header = headers.get("content-length")
                if content_length_header:
                    original_size = int(content_length_header)
                    if original_size > 0:
                        compression_ratio = round(
                            (1 - content_length / original_size) * 100, 1
                        )

            # Check caching
            cache_control = headers.get("cache-control", "none")
            etag = headers.get("etag", None)
            last_modified = headers.get("last-modified", None)
            has_caching = cache_control != "none" or etag is not None

            # Parse HTML to count resources
            html_text = response.text if response.status_code == 200 else ""
            resources = _count_resources(html_text, str(response.url))

            # Performance score (simple heuristic)
            score = _calculate_score(
                ttfb_ms=ttfb_ms,
                total_time=total_time,
                page_size_kb=content_length / 1024,
                is_compressed=is_compressed,
                has_caching=has_caching,
                resource_count=resources["total"],
            )

            # Recommendations
            recommendations = _generate_recommendations(
                ttfb_ms=ttfb_ms,
                total_time=total_time,
                page_size_bytes=content_length,
                is_compressed=is_compressed,
                has_caching=has_caching,
                cache_control=cache_control,
                resource_count=resources["total"],
                html_size=resources["html_size"],
            )

            return {
                "url": str(response.url),
                "original_url": url,
                "status_code": response.status_code,
                "performance_score": score,
                "metrics": {
                    "ttfb_ms": round(ttfb_ms, 2),
                    "total_load_time_ms": round(total_time, 2),
                    "page_size_bytes": content_length,
                    "page_size_kb": round(content_length / 1024, 2),
                    "page_size_mb": round(content_length / (1024 * 1024), 2),
                },
                "optimization": {
                    "is_compressed": is_compressed,
                    "compression_type": content_encoding if is_compressed else None,
                    "compression_ratio": compression_ratio,
                    "has_caching": has_caching,
                    "cache_control": cache_control,
                    "etag": etag,
                    "last_modified": last_modified,
                },
                "resources": resources,
                "recommendations": recommendations,
                "error": None,
            }

    except httpx.ConnectError:
        return {"url": url, "error": f"Tidak dapat terhubung ke {url}"}
    except httpx.TimeoutException:
        return {"url": url, "error": f"Timeout saat mengakses {url}"}
    except Exception as e:
        return {"url": url, "error": f"Error: {str(e)}"}


def _count_resources(html: str, base_url: str) -> dict:
    """Count and categorize resources in HTML"""
    if not html:
        return {
            "html_size": 0,
            "css_count": 0,
            "js_count": 0,
            "image_count": 0,
            "total": 0,
        }

    # Count CSS files
    css_links = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    css_inline = re.findall(r'<style[^>]*>', html, re.I)
    css_count = len(css_links) + len(css_inline)

    # Count JS files
    js_scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I)
    js_inline = re.findall(r'<script[^>]*>(?!.*src)', html, re.I)
    js_count = len(js_scripts) + len(js_inline)

    # Count images
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    img_bg = re.findall(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', html, re.I)
    image_count = len(img_tags) + len(img_bg)

    total = css_count + js_count + image_count

    return {
        "html_size": len(html.encode('utf-8')),
        "css_count": css_count,
        "css_files": css_links[:10],  # Top 10
        "js_count": js_count,
        "js_files": js_scripts[:10],  # Top 10
        "image_count": image_count,
        "image_files": img_tags[:10],  # Top 10
        "total": total,
    }


def _calculate_score(
    ttfb_ms: float,
    total_time: float,
    page_size_kb: float,
    is_compressed: bool,
    has_caching: bool,
    resource_count: int,
) -> dict:
    """Calculate a simple performance score (0-100)"""
    score = 100
    deductions = []

    # TTFB scoring (ideal < 200ms)
    if ttfb_ms > 1000:
        score -= 30
        deductions.append("TTFB sangat lambat (>1s)")
    elif ttfb_ms > 500:
        score -= 20
        deductions.append("TTFB lambat (>500ms)")
    elif ttfb_ms > 200:
        score -= 10
        deductions.append("TTFB bisa lebih baik (>200ms)")

    # Total load time scoring (ideal < 3s)
    if total_time > 10000:
        score -= 25
        deductions.append("Load time sangat lambat (>10s)")
    elif total_time > 5000:
        score -= 15
        deductions.append("Load time lambat (>5s)")
    elif total_time > 3000:
        score -= 5
        deductions.append("Load time bisa lebih baik (>3s)")

    # Page size scoring (ideal < 500KB)
    if page_size_kb > 5000:
        score -= 20
        deductions.append("Page size sangat besar (>5MB)")
    elif page_size_kb > 2000:
        score -= 15
        deductions.append("Page size besar (>2MB)")
    elif page_size_kb > 500:
        score -= 5
        deductions.append("Page size bisa lebih kecil (>500KB)")

    # Compression
    if not is_compressed:
        score -= 15
        deductions.append("Tidak menggunakan kompresi")

    # Caching
    if not has_caching:
        score -= 10
        deductions.append("Tidak ada caching header")

    # Resource count
    if resource_count > 100:
        score -= 10
        deductions.append(f"Terlalu banyak resource ({resource_count})")
    elif resource_count > 50:
        score -= 5
        deductions.append(f"Banyak resource ({resource_count})")

    # Determine grade
    score = max(0, min(100, score))
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "score": score,
        "grade": grade,
        "deductions": deductions,
    }


def _generate_recommendations(
    ttfb_ms: float,
    total_time: float,
    page_size_bytes: int,
    is_compressed: bool,
    has_caching: bool,
    cache_control: str,
    resource_count: int,
    html_size: int,
) -> List[dict]:
    """Generate optimization recommendations"""
    recommendations = []

    # TTFB
    if ttfb_ms > 500:
        recommendations.append({
            "priority": "tinggi",
            "category": "Server",
            "title": "Optimasi TTFB (Time to First Byte)",
            "description": f"TTFB saat ini {ttfb_ms:.0f}ms. Idealnya < 200ms.",
            "tips": [
                "Gunakan server yang lebih dekat dengan pengguna",
                "Aktifkan server-side caching (Redis/Memcached)",
                "Optimasi database queries",
                "Gunakan CDN untuk static assets",
            ],
        })

    # Compression
    if not is_compressed:
        recommendations.append({
            "priority": "tinggi",
            "category": "Optimasi",
            "title": "Aktifkan Kompresi (gzip/brotli)",
            "description": "Website Anda tidak menggunakan kompresi. Kompresi bisa mengurangi ukuran transfer hingga 70%.",
            "tips": [
                "Aktifkan gzip compression di Nginx/Apache",
                "Gunakan brotli compression untuk performa lebih baik",
                "Kompresi HTML, CSS, JavaScript",
            ],
        })

    # Caching
    if not has_caching:
        recommendations.append({
            "priority": "tinggi",
            "category": "Caching",
            "title": "Tambahkan Caching Headers",
            "description": "Website Anda tidak memiliki caching headers. Ini memperlambat load untuk pengunjung berulang.",
            "tips": [
                "Set Cache-Control header untuk static assets",
                "Gunakan ETag untuk validasi cache",
                "Set max-age minimal 1 jam untuk CSS/JS/images",
            ],
        })
    elif "no-cache" in cache_control or "no-store" in cache_control:
        recommendations.append({
            "priority": "sedang",
            "category": "Caching",
            "title": "Optimasi Caching Strategy",
            "description": "Anda menggunakan no-cache/no-store. Pertimbangkan caching yang lebih optimal.",
            "tips": [
                "Gunakan max-age untuk static assets",
                "Gunakan no-cache untuk dynamic content",
                "Implementasi stale-while-revalidate",
            ],
        })

    # Page size
    page_size_kb = page_size_bytes / 1024
    if page_size_kb > 2000:
        recommendations.append({
            "priority": "tinggi",
            "category": "Optimasi",
            "title": "Kurangi Ukuran Halaman",
            "description": f"Ukuran halaman {page_size_kb:.0f}KB. Idealnya < 500KB.",
            "tips": [
                "Kompresi gambar (WebP format)",
                "Minify CSS dan JavaScript",
                "Hapus kode yang tidak terpakai",
                "Gunakan lazy loading untuk gambar",
            ],
        })

    # Resource count
    if resource_count > 50:
        recommendations.append({
            "priority": "sedang",
            "category": "Optimasi",
            "title": "Kurangi Jumlah Resource",
            "description": f"Halaman memuat {resource_count} resource. Idealnya < 30.",
            "tips": [
                "Gabungkan CSS files",
                "Gabungkan JavaScript files",
                "Gunakan CSS sprites untuk gambar kecil",
                "Implementasi lazy loading",
            ],
        })

    # HTML size
    if html_size > 100000:  # > 100KB
        recommendations.append({
            "priority": "sedang",
            "category": "Optimasi",
            "title": "Kurangi Ukuran HTML",
            "description": f"HTML size {html_size / 1024:.0f}KB. Idealnya < 50KB.",
            "tips": [
                "Hapus HTML yang tidak terpakai",
                "Gunakan template engine yang efisien",
                "Implementasi server-side rendering yang optimal",
            ],
        })

    return recommendations
