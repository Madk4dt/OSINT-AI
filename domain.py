# domain.py
import dns.resolver
import whois
from utils import t, check_internet, is_valid_domain
from config import SOURCES_DB

def domain_info(domain):
    if not check_internet(): return t("no_internet"), []
    if not is_valid_domain(domain): return t("invalid_domain"), []
    lines = [t("domain_title", domain), ""]
    try:
        w = whois.whois(domain)
        lines.append(t("domain_creation", w.creation_date))
        lines.append(t("domain_expiration", w.expiration_date))
        lines.append(t("domain_registrar", w.registrar))
        lines.append(t("domain_nameservers", w.name_servers))
    except Exception as e:
        lines.append(t("domain_whois_error", str(e)))
    try:
        a = dns.resolver.resolve(domain, 'A')
        lines.append(t("domain_a_records", [r.address for r in a]))
    except:
        pass
    return "\n".join(lines), SOURCES_DB.get("domain", [])

def subdomain_search(domain):
    subs = ['www','mail','ftp','localhost','webmail','smtp','pop','ns1','ns2','cpanel','whm',
            'autodiscover','autoconfig','admin','blog','dev','api','test','vpn','forum','shop']
    lines = [t("subdomain_title", domain), ""]
    found = False
    for sub in subs:
        full = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(full, 'A')
            lines.append(t("subdomain_found", full))
            found = True
        except:
            continue
    if not found:
        lines.append("Не найдено.")
    return "\n".join(lines), SOURCES_DB.get("subdomain", [])

def dns_recon(domain):
    if not check_internet():
        return t("no_internet"), []
    lines = [f"DNS-записи для {domain}"]
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            lines.append(f"{rtype}:")
            for r in answers:
                lines.append(f"  {r.to_text()}")
        except dns.resolver.NoAnswer:
            lines.append(f"{rtype}: нет записей")
        except Exception as e:
            lines.append(f"{rtype}: ошибка - {e}")
    return "\n".join(lines), SOURCES_DB.get("dnsrecon", [])