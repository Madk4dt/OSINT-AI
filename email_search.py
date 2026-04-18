# email.py
import requests
import dns.resolver
from utils import t, check_internet, is_valid_email
from config import SOURCES_DB

def email_lookup(email):
    if not check_internet(): return t("no_internet"), []
    if not is_valid_email(email): return t("invalid_email"), []
    lines = [t("email_title", email), ""]
    try:
        r = requests.get(f"https://emailrep.io/{email}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            lines.append(t("email_reputation", data.get('reputation', 'N/A')))
            if 'breaches' in data.get('details', {}):
                lines.append(t("email_breaches", ', '.join(data['details']['breaches'][:3])))
            lines.append("")
        else:
            lines.append(t("email_error", r.status_code))
    except Exception as e:
        lines.append(t("email_error", str(e)))
    domain = email.split('@')[-1]
    try:
        mx = dns.resolver.resolve(domain, 'MX')
        lines.append(t("email_mx", [str(r.exchange) for r in mx]))
    except:
        lines.append(t("email_mx_error", domain))
    return "\n".join(lines), SOURCES_DB.get("email", [])