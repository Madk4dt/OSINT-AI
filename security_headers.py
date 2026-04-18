# security_headers.py
import requests
from utils import t, check_internet
from config import SOURCES_DB

def analyze_security_headers(url):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    lines = [f"🔒 Security Headers Analysis: {url}", ""]
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "OSINT-SecCheck"})
        headers = r.headers
        checks = {
            "Strict-Transport-Security": "HSTS (защита от SSL stripping)",
            "Content-Security-Policy": "CSP (защита от XSS)",
            "X-Frame-Options": "Защита от clickjacking",
            "X-Content-Type-Options": "Защита от MIME sniffing",
            "Referrer-Policy": "Контроль referer",
            "Permissions-Policy": "Ограничение API браузера",
            "X-XSS-Protection": "Старая защита XSS",
            "Cross-Origin-Embedder-Policy": "COEP",
            "Cross-Origin-Opener-Policy": "COOP",
            "Cross-Origin-Resource-Policy": "CORP"
        }
        for h, desc in checks.items():
            value = headers.get(h, "❌ отсутствует")
            if value == "❌ отсутствует":
                lines.append(f"[!] {h}: {value} — {desc}")
            else:
                lines.append(f"[+] {h}: {value}")
        # Дополнительно: проверка на unsafe-inline в CSP
        csp = headers.get("Content-Security-Policy", "")
        if "unsafe-inline" in csp:
            lines.append("[!] CSP использует unsafe-inline (риск XSS)")
        if "unsafe-eval" in csp:
            lines.append("[!] CSP использует unsafe-eval (риск инъекций)")
        if not headers.get("Strict-Transport-Security"):
            lines.append("[!] HSTS отсутствует — возможен SSL strip")
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), SOURCES_DB.get("security_headers", [])

# Команда: secheaders <url>