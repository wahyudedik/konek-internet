"""Technology Detector service - Deteksi teknologi yang digunakan website"""
import re
import asyncio
from typing import Dict, Any, List, Optional
from app.utils.cache import cached

try:
    import httpx
except ImportError:
    httpx = None


# Technology signatures - dictionary of detection patterns
TECH_SIGNATURES = {
    # CMS
    "WordPress": {
        "category": "CMS",
        "patterns": ["wp-content", "wp-includes", "wp-json", "xmlrpc.php"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": [],
    },
    "Joomla": {
        "category": "CMS",
        "patterns": ["/media/jui/", "com_content", "Joomla!"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": [],
    },
    "Drupal": {
        "category": "CMS",
        "patterns": ["drupal.js", "Drupal.settings", "sites/default/files"],
        "meta_patterns": ["drupal"],
        "header_patterns": ["X-Generator: Drupal"],
        "js_patterns": [],
    },
    "Shopify": {
        "category": "E-Commerce",
        "patterns": ["cdn.shopify.com", "Shopify.theme"],
        "meta_patterns": [],
        "header_patterns": ["x-shopify-stage"],
        "js_patterns": [],
    },
    "WooCommerce": {
        "category": "E-Commerce",
        "patterns": ["woocommerce", "wc-"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["woocommerce"],
    },

    # Frameworks
    "Laravel": {
        "category": "Framework",
        "patterns": ["laravel", "csrf-token"],
        "meta_patterns": [],
        "header_patterns": ["X-Powered-By: Laravel"],
        "js_patterns": [],
    },
    "Django": {
        "category": "Framework",
        "patterns": ["csrfmiddlewaretoken", "__admin_media_prefix__"],
        "meta_patterns": [],
        "header_patterns": ["X-Frame-Options: DENY"],
        "js_patterns": [],
    },
    "Ruby on Rails": {
        "category": "Framework",
        "patterns": ["csrf-param", "csrf-token"],
        "meta_patterns": [],
        "header_patterns": ["X-Powered-By: Phusion Passenger", "X-Runtime"],
        "js_patterns": [],
    },
    "Express.js": {
        "category": "Framework",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["X-Powered-By: Express"],
        "js_patterns": [],
    },
    "ASP.NET": {
        "category": "Framework",
        "patterns": ["__VIEWSTATE", "__EVENTVALIDATION", "asp.net"],
        "meta_patterns": ["asp.net"],
        "header_patterns": ["X-Powered-By: ASP.NET", "X-AspNet-Version"],
        "js_patterns": [],
    },
    "Spring Boot": {
        "category": "Framework",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["X-Application-Context"],
        "js_patterns": [],
    },

    # JavaScript Frameworks
    "React": {
        "category": "JavaScript Framework",
        "patterns": ["react", "reactroot", "reactroot"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["react", "reactdom"],
    },
    "Vue.js": {
        "category": "JavaScript Framework",
        "patterns": ["vue.js", "vue.min.js", "v-cloak"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["vue.js", "vue.min.js"],
    },
    "Angular": {
        "category": "JavaScript Framework",
        "patterns": ["ng-version", "ng-app", "angular"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["angular"],
    },
    "Svelte": {
        "category": "JavaScript Framework",
        "patterns": ["svelte"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["svelte"],
    },
    "Next.js": {
        "category": "JavaScript Framework",
        "patterns": ["__NEXT_DATA__", "_next/static"],
        "meta_patterns": [],
        "header_patterns": ["x-powered-by: Next.js"],
        "js_patterns": ["next"],
    },
    "Nuxt.js": {
        "category": "JavaScript Framework",
        "patterns": ["__NUXT__", "_nuxt/"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["nuxt"],
    },
    "Gatsby": {
        "category": "JavaScript Framework",
        "patterns": ["gatsby", "___gatsby"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["gatsby"],
    },

    # CSS Frameworks
    "Bootstrap": {
        "category": "CSS Framework",
        "patterns": ["bootstrap.min.css", "bootstrap.min.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["bootstrap"],
    },
    "Tailwind CSS": {
        "category": "CSS Framework",
        "patterns": ["tailwindcss", "tailwind.min.css"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["tailwindcss"],
    },
    "Bulma": {
        "category": "CSS Framework",
        "patterns": ["bulma.min.css", "bulma.css"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": [],
    },
    "Materialize": {
        "category": "CSS Framework",
        "patterns": ["materialize.min.css", "materialize.min.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["materialize"],
    },

    # Analytics & Tracking
    "Google Analytics": {
        "category": "Analytics",
        "patterns": ["google-analytics.com", "googletagmanager.com/gtag", "ga.js", "analytics.js", "gtag("],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["google-analytics", "gtag"],
    },
    "Google Tag Manager": {
        "category": "Analytics",
        "patterns": ["googletagmanager.com/gtm.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["googletagmanager"],
    },
    "Facebook Pixel": {
        "category": "Analytics",
        "patterns": ["connect.facebook.net", "fbq("],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["facebook.net"],
    },
    "Hotjar": {
        "category": "Analytics",
        "patterns": ["hotjar.com", "hj("],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["hotjar"],
    },
    "Mixpanel": {
        "category": "Analytics",
        "patterns": ["mixpanel.com", "mixpanel.init"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["mixpanel"],
    },

    # Web Server
    "Nginx": {
        "category": "Web Server",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["Server: nginx"],
        "js_patterns": [],
    },
    "Apache": {
        "category": "Web Server",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["Server: Apache"],
        "js_patterns": [],
    },
    "LiteSpeed": {
        "category": "Web Server",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["Server: LiteSpeed"],
        "js_patterns": [],
    },
    "Cloudflare": {
        "category": "CDN",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["Server: cloudflare"],
        "js_patterns": [],
    },
    "Microsoft IIS": {
        "category": "Web Server",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["Server: Microsoft-IIS"],
        "js_patterns": [],
    },

    # Hosting / Platform
    "Vercel": {
        "category": "Hosting",
        "patterns": [],
        "meta_patterns": [],
        "header_patterns": ["x-vercel-id", "Server: Vercel"],
        "js_patterns": [],
    },
    "Netlify": {
        "category": "Hosting",
        "patterns": ["netlify"],
        "meta_patterns": [],
        "header_patterns": ["Server: Netlify"],
        "js_patterns": [],
    },
    "Firebase": {
        "category": "Hosting",
        "patterns": ["firebaseio.com", "firebaseapp.com"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["firebase"],
    },

    # Libraries
    "jQuery": {
        "category": "JavaScript Library",
        "patterns": ["jquery.min.js", "jquery.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["jquery"],
    },
    "Lodash": {
        "category": "JavaScript Library",
        "patterns": ["lodash.min.js", "lodash.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["lodash"],
    },
    "Moment.js": {
        "category": "JavaScript Library",
        "patterns": ["moment.min.js", "moment.js"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["moment"],
    },

    # Security
    "reCAPTCHA": {
        "category": "Security",
        "patterns": ["recaptcha", "google.com/recaptcha"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["recaptcha"],
    },
    "hCaptcha": {
        "category": "Security",
        "patterns": ["hcaptcha.com"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["hcaptcha"],
    },

    # Email Marketing
    "Mailchimp": {
        "category": "Email Marketing",
        "patterns": ["list-manage.com", "mailchimp.com"],
        "meta_patterns": [],
        "header_patterns": [],
        "js_patterns": ["mailchimp"],
    },
}


@cached(ttl=3600)
async def detect_technologies(url: str) -> Dict[str, Any]:
    """
    Technology Detector - Deteksi teknologi yang digunakan website.
    Menganalisis HTML, HTTP headers, dan JavaScript untuk mengidentifikasi
    CMS, framework, library, analytics, dan lainnya.
    """
    if httpx is None:
        return {"url": url, "technologies": [], "error": "httpx tidak terinstall"}

    # Normalize URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        async with httpx.AsyncClient(
            verify=False,
            follow_redirects=True,
            timeout=15,
        ) as client:
            response = await client.get(url)

            # Get HTML content
            html_content = response.text.lower() if response.text else ""

            # Get headers
            headers = dict(response.headers)
            headers_lower = {k.lower(): v.lower() for k, v in headers.items()}

            # Detect technologies
            detected = []

            for tech_name, signatures in TECH_SIGNATURES.items():
                confidence = 0
                evidence = []

                # Check HTML patterns
                for pattern in signatures["patterns"]:
                    if pattern.lower() in html_content:
                        confidence += 30
                        evidence.append(f"HTML: {pattern}")

                # Check meta patterns
                for pattern in signatures["meta_patterns"]:
                    if pattern.lower() in html_content:
                        confidence += 20
                        evidence.append(f"Meta: {pattern}")

                # Check header patterns
                for pattern in signatures["header_patterns"]:
                    header_name = pattern.split(":")[0].strip().lower()
                    header_value = pattern.split(":", 1)[1].strip().lower() if ":" in pattern else ""
                    if header_name in headers_lower:
                        if header_value and header_value in headers_lower[header_name]:
                            confidence += 40
                            evidence.append(f"Header: {pattern}")
                        elif not header_value:
                            confidence += 40
                            evidence.append(f"Header: {pattern}")

                # Check JS patterns
                for pattern in signatures["js_patterns"]:
                    if pattern.lower() in html_content:
                        confidence += 25
                        evidence.append(f"JS: {pattern}")

                if confidence > 0:
                    detected.append({
                        "name": tech_name,
                        "category": signatures["category"],
                        "confidence": min(confidence, 100),
                        "evidence": evidence,
                    })

            # Sort by confidence
            detected.sort(key=lambda x: x["confidence"], reverse=True)

            # Extract additional info
            server = headers.get("Server", "Unknown")
            powered_by = headers.get("X-Powered-By", None)
            content_type = headers.get("Content-Type", "Unknown")

            return {
                "url": str(response.url),
                "final_url": str(response.url),
                "status_code": response.status_code,
                "server": server,
                "powered_by": powered_by,
                "content_type": content_type,
                "technologies": detected,
                "total_detected": len(detected),
                "categories": _group_by_category(detected),
                "error": None,
            }

    except httpx.ConnectError:
        return {
            "url": url,
            "technologies": [],
            "error": f"Tidak dapat terhubung ke {url}",
        }
    except httpx.TimeoutException:
        return {
            "url": url,
            "technologies": [],
            "error": f"Timeout saat mengakses {url}",
        }
    except Exception as e:
        return {
            "url": url,
            "technologies": [],
            "error": f"Error: {str(e)}",
        }


def _group_by_category(technologies: List[dict]) -> Dict[str, List[str]]:
    """Group detected technologies by category"""
    categories = {}
    for tech in technologies:
        cat = tech["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tech["name"])
    return categories
