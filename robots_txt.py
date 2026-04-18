# robots_txt.py
# USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION
import requests
from urllib.parse import urljoin
from utils import check_internet

def get_robots_txt(url):
    if not check_internet():
        return "Нет интернета", []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    robots_url = urljoin(url, '/robots.txt')
    try:
        r = requests.get(robots_url, timeout=10)
        if r.status_code == 200:
            return f"robots.txt для {url}\n\n{r.text}", []
        else:
            return f"robots.txt не найден (код {r.status_code})", []
    except Exception as e:
        return f"Ошибка: {e}", []