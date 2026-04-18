# git_discovery.py
# USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION
import requests
from urllib.parse import urljoin
from utils import check_internet

def git_discovery(url):
    if not check_internet():
        return "Нет интернета", []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    git_url = urljoin(url, '/.git/config')
    try:
        r = requests.get(git_url, timeout=10)
        if r.status_code == 200 and '[core]' in r.text:
            return f"[!] Найден .git/config по адресу {git_url}\nВозможна утечка исходного кода!", []
        else:
            return f".git/config не обнаружен (код {r.status_code})", []
    except Exception as e:
        return f"Ошибка: {e}", []