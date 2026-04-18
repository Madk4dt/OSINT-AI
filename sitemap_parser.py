# sitemap_parser.py
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from utils import t, check_internet

def parse_sitemap(url):
    if not check_internet():
        return t("no_internet"), []
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    # Нормализуем URL к корню сайта
    if url.endswith('/sitemap.xml'):
        sitemap_url = url
    else:
        sitemap_url = url.rstrip('/') + '/sitemap.xml'
    lines = [f"🗺️ Sitemap: {sitemap_url}", ""]
    try:
        r = requests.get(sitemap_url, timeout=10)
        if r.status_code != 200:
            return f"❌ Sitemap не найден (код {r.status_code})", []
        root = ET.fromstring(r.content)
        # Namespace может быть
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []
        for loc in root.findall('.//ns:loc', ns):
            urls.append(loc.text)
        if not urls:
            # возможно, sitemap index
            for sitemap in root.findall('.//ns:sitemap/ns:loc', ns):
                sub_r = requests.get(sitemap.text, timeout=10)
                if sub_r.status_code == 200:
                    sub_root = ET.fromstring(sub_r.content)
                    for sub_loc in sub_root.findall('.//ns:loc', ns):
                        urls.append(sub_loc.text)
        lines.append(f"Найдено URL: {len(urls)}")
        for i, u in enumerate(urls[:50]):
            lines.append(f"  {i+1}. {u}")
        if len(urls) > 50:
            lines.append(f"  ... и ещё {len(urls)-50} URL")
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), []

# Команда: sitemap <url>