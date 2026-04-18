# ip.py
import requests
from utils import t, check_internet, is_valid_ip
from config import SOURCES_DB

def ip_info(ip):
    if not check_internet(): return t("no_internet"), []
    if not is_valid_ip(ip): return t("invalid_ip"), []
    lines = [t("ip_title", ip), ""]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()
        if data.get('status') == 'success':
            lines.append(t("ip_country", data.get('country')))
            lines.append(t("ip_city", data.get('city')))
            lines.append(t("ip_isp", data.get('isp')))
            lines.append(t("ip_coords", data.get('lat'), data.get('lon')))
        else:
            lines.append(t("ip_error", data.get('message')))
    except Exception as e:
        lines.append(t("ip_api_error", str(e)))
    return "\n".join(lines), SOURCES_DB.get("ip", [])