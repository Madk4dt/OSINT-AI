# github.py
import requests
from bs4 import BeautifulSoup
from utils import t
from config import SOURCES_DB

def github_search(username):
    lines = [t("github_title", username), ""]
    url = f"https://github.com/{username}"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            repo_span = soup.find('span', class_='Counter')
            repos = repo_span.text.strip() if repo_span else '?'
            lines.append(t("github_repos", repos))
            followers_a = soup.find('a', href=f'/{username}?tab=followers')
            followers = followers_a.find('span', class_='text-bold').text.strip() if followers_a else '?'
            lines.append(t("github_followers", followers))
            following_a = soup.find('a', href=f'/{username}?tab=following')
            following = following_a.find('span', class_='text-bold').text.strip() if following_a else '?'
            lines.append(t("github_following", following))
        else:
            lines.append(t("github_error"))
    except:
        lines.append(t("github_error"))
    return "\n".join(lines), SOURCES_DB.get("github", [])