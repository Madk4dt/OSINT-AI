# cookie_analyzer.py
# USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION
import requests
from utils import check_internet

def analyze_cookies(url):
    if not check_internet():
        return "Нет интернета", []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    try:
        r = requests.get(url, timeout=10)
        lines = [f"Cookie анализ: {url}", ""]
        if not r.cookies:
            lines.append("Куки не установлены")
        else:
            for cookie in r.cookies:
                attrs = []
                if not cookie.secure:
                    attrs.append("Нет Secure")
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    attrs.append("Нет HttpOnly")
                if cookie.get_nonstandard_attr('SameSite') not in ('Strict', 'Lax'):
                    attrs.append("SameSite отсутствует или слабый")
                status = "[!]" + ", ".join(attrs) if attrs else "[+] безопасный"
                lines.append(f"{cookie.name}: {status}")
        return "\n".join(lines), []
    except Exception as e:
        return f"Ошибка: {e}", []