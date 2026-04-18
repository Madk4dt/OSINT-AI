# html_comment_extractor.py
# USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION
import requests
import re
from utils import check_internet

def extract_comments(url):
    if not check_internet():
        return "Нет интернета", []
    if not url.startswith(('http://','https://')):
        url = 'https://' + url
    try:
        r = requests.get(url, timeout=10)
        comments = re.findall(r'<!--(.*?)-->', r.text, re.DOTALL)
        if comments:
            lines = [f"Найдено HTML-комментариев: {len(comments)}", ""]
            for i, c in enumerate(comments[:20]):
                lines.append(f"{i+1}. {c.strip()[:200]}")
            return "\n".join(lines), []
        else:
            return "Комментариев не найдено", []
    except Exception as e:
        return f"Ошибка: {e}", []