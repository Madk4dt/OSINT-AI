# username.py (версия 6.0)
import requests
import concurrent.futures
from utils import t, check_internet, is_valid_username, show_progress, print_info
from config import SOURCES_DB

def username_search(username):
    if not check_internet():
        return t("no_internet"), []
    if not is_valid_username(username):
        return t("invalid_username"), []
    
    lines = [t("username_title", username), ""]
    
    sites = {
        # Основные соцсети и платформы
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Telegram": f"https://t.me/{username}",
        "VK": f"https://vk.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Discord": f"https://discord.com/users/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Tumblr": f"https://{username}.tumblr.com",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Medium": f"https://medium.com/@{username}",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Myspace": f"https://myspace.com/{username}",
        "Threads": f"https://www.threads.net/@{username}",
        "Signal": f"https://signal.me/#p/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Bitbucket": f"https://bitbucket.org/{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
        "StackOverflow": f"https://stackoverflow.com/users/@{username}",
        "LeetCode": f"https://leetcode.com/{username}/",
        "Codeforces": f"https://codeforces.com/profile/{username}",
        "Replit": f"https://replit.com/@{username}",
        "PyPI": f"https://pypi.org/user/{username}/",
        "NPM": f"https://www.npmjs.com/~{username}",
        "DockerHub": f"https://hub.docker.com/u/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "Pastebin": f"https://pastebin.com/u/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Chess": f"https://www.chess.com/member/{username}",
        "Codewars": f"https://www.codewars.com/users/{username}",
        "HackTheBox": f"https://www.hackthebox.com/home/users/profile/{username}",
        "Bugcrowd": f"https://bugcrowd.com/{username}",
        "HackerOne": f"https://hackerone.com/{username}",
        "Gravatar": f"https://en.gravatar.com/{username}",
        "About.me": f"https://about.me/{username}",
        "SlideShare": f"https://www.slideshare.net/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Mixcloud": f"https://www.mixcloud.com/{username}",
        "Codecademy": f"https://www.codecademy.com/profiles/{username}",
        "Wattpad": f"https://www.wattpad.com/user/{username}",
        "Disqus": f"https://disqus.com/by/{username}/",
        "Patreon": f"https://www.patreon.com/{username}",
        "Venmo": f"https://venmo.com/{username}",
        "CashApp": f"https://cash.app/@{username}",
        "PayPal.Me": f"https://paypal.me/{username}",
        "Issuu": f"https://issuu.com/{username}",
        "Mastodon": f"https://mastodon.social/@{username}",
    }
    
    found = False
    
    def check_site(name, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            r = requests.get(url, timeout=5, headers=headers, allow_redirects=True)
            return (name, url, r.status_code, None)
        except Exception as e:
            return (name, url, None, str(e))
    
    total = len(sites)
    completed = 0
    print_info(f"Проверка {total} сайтов...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_site = {executor.submit(check_site, name, url): name for name, url in sites.items()}
        for future in concurrent.futures.as_completed(future_to_site):
            name, url, status, error = future.result()
            completed += 1
            show_progress(completed, total, prefix="Поиск username", suffix=f" ({name})")
            if error:
                lines.append(t("username_error", name))
            elif status == 200:
                lines.append(t("username_found", name, url))
                found = True
            elif status == 404:
                lines.append(t("username_not_found", name, status))
            else:
                if "blocked" in str(error) or "login" in str(error):
                    lines.append(f"[?] {name}: возможно существует, но требует входа (код {status})")
                else:
                    lines.append(t("username_not_found", name, status))
    
    if not found:
        lines.append(t("username_none"))
    
    return "\n".join(lines), SOURCES_DB.get("username", [])