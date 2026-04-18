# web.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import t, check_internet, show_progress
from config import SOURCES_DB

def parse_website(url, depth=1):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    
    lines = [t("parse_title", url), ""]
    emails, phones, usernames = set(), set(), set()
    visited = set()
    to_visit = [(url, 0)]
    email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_re = r'\+?\d[\d\s\-\(\)]{8,}\d'
    user_re = r'(?:twitter\.com/|instagram\.com/|t\.me/|vk\.com/)([a-zA-Z0-9_]+)'
    
    def process_page(cur, d):
        if cur in visited or d > depth:
            return None
        visited.add(cur)
        try:
            r = requests.get(cur, timeout=10, headers={"User-Agent": "OSINT-Parser"})
            if r.status_code != 200:
                return None
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text()
            page_emails = set(re.findall(email_re, text))
            page_phones = set()
            for m in re.findall(phone_re, text):
                if len(re.sub(r'\D', '', m)) >= 10:
                    page_phones.add(m)
            page_usernames = set()
            for a in soup.find_all('a', href=True):
                m = re.search(user_re, a['href'])
                if m:
                    page_usernames.add(m.group(1))
            links = []
            if d < depth:
                for a in soup.find_all('a', href=True):
                    link = urljoin(cur, a['href'])
                    if link.startswith(('http://','https://')) and link not in visited:
                        links.append((link, d+1))
            return {
                'emails': page_emails,
                'phones': page_phones,
                'usernames': page_usernames,
                'links': links
            }
        except:
            return None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while to_visit and len(visited) < 20:
            batch = to_visit[:10]
            to_visit = to_visit[10:]
            futures = [executor.submit(process_page, cur, d) for cur, d in batch]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    emails.update(result['emails'])
                    phones.update(result['phones'])
                    usernames.update(result['usernames'])
                    to_visit.extend(result['links'])
                show_progress(len(visited), 20, prefix="Парсинг страниц", suffix=f" (обработано {len(visited)})")
    
    lines.append(t("parse_emails"))
    for e in list(emails)[:20]:
        lines.append(f"  {e}")
    lines.append(t("parse_phones"))
    for p in list(phones)[:20]:
        lines.append(f"  {p}")
    lines.append(t("parse_usernames"))
    for u in list(usernames)[:20]:
        lines.append(f"  {u}")
    lines.append(t("parse_links", len(visited)))
    return "\n".join(lines), SOURCES_DB.get("parse", [])

def http_headers(url):
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    lines = [t("httpheaders_title", url), ""]
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "OSINT-AI"})
        for k,v in r.headers.items():
            lines.append(f"{k}: {v}")
    except Exception as e:
        lines.append(t("error_prefix", str(e)))
    return "\n".join(lines), SOURCES_DB.get("httpheaders", [])

def web_technologies(url):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    lines = [f"Технологии сайта {url}"]
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        server = r.headers.get('Server', 'не указан')
        x_powered = r.headers.get('X-Powered-By', 'не указан')
        lines.append(f"Сервер: {server}")
        lines.append(f"X-Powered-By: {x_powered}")
        soup = BeautifulSoup(r.text, 'html.parser')
        generators = soup.find_all('meta', attrs={'name': 'generator'})
        if generators:
            lines.append("CMS/Генератор: " + generators[0].get('content', 'неизвестно'))
        scripts = soup.find_all('script', src=True)
        js_libs = set()
        for s in scripts:
            src = s['src'].lower()
            if 'jquery' in src: js_libs.add('jQuery')
            if 'bootstrap' in src: js_libs.add('Bootstrap')
            if 'react' in src: js_libs.add('React')
            if 'vue' in src: js_libs.add('Vue.js')
            if 'angular' in src: js_libs.add('Angular')
        if js_libs:
            lines.append("JS библиотеки: " + ', '.join(js_libs))
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), SOURCES_DB.get("webtech", [])

def email_harvest(url):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    lines = [f"Сбор email с {url}"]
    emails = set()
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', r.text)
        for email in found:
            emails.add(email.lower())
        lines.append(f"Найдено {len(emails)} уникальных email:")
        for e in sorted(emails)[:30]:
            lines.append(f"  {e}")
        if len(emails) > 30:
            lines.append(f"  ... и ещё {len(emails)-30}")
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), SOURCES_DB.get("emailharvest", [])

def extract_from_url(url):
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    lines = [t("extract_title", url), ""]
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "OSINT-Extract"})
        soup = BeautifulSoup(r.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            h = a['href']
            if h.startswith(('http://','https://')):
                links.add(h)
        lines.append(t("extract_links"))
        for link in list(links)[:20]:
            lines.append(f"  {link}")
        forms = soup.find_all('form')
        lines.append(t("extract_forms"))
        for form in forms[:10]:
            action = form.get('action','')
            method = form.get('method','get')
            lines.append(f"  {method.upper()} {action}")
        scripts = soup.find_all('script', src=True)
        lines.append(t("extract_scripts"))
        for script in scripts[:10]:
            lines.append(f"  {script['src']}")
    except Exception as e:
        lines.append(t("extract_error", str(e)))
    return "\n".join(lines), SOURCES_DB.get("extract", [])