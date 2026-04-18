# js_analyzer.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import t, check_internet

def analyze_js(url):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    lines = [f"JavaScript Analysis: {url}", ""]
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        found_keys = set()
        pattern_api = re.compile(r'(["\']?[A-Za-z0-9_]{20,}["\']?)\s*[:=]\s*(["\'])([A-Za-z0-9_\-]{20,})\2')
        pattern_email = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        for script in scripts[:20]:
            src = script['src']
            full_url = urljoin(url, src)
            try:
                js_r = requests.get(full_url, timeout=10)
                js_text = js_r.text
                # Поиск API ключей (простые паттерны)
                for match in pattern_api.findall(js_text):
                    found_keys.add(match[0] + "=" + match[2][:10] + "...")
                for email in pattern_email.findall(js_text):
                    found_keys.add(f"EMAIL: {email}")
                # Дополнительно: aws keys, google api
                if 'AIza' in js_text:
                    found_keys.add("Возможный Google API ключ (AIza...)")
                if 'AKIA' in js_text:
                    found_keys.add("Возможный AWS ключ (AKIA...)")
            except:
                continue
        if found_keys:
            lines.append("Потенциально чувствительные данные в JS:")
            for item in found_keys:
                lines.append(f"  {item}")
        else:
            lines.append("Ничего не найдено.")
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), []

# Команда: jsanalyze <url>