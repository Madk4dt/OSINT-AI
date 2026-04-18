# ssl.py
import socket
import ssl as ssl_lib
from utils import t
from config import SOURCES_DB

def ssl_info(domain):
    lines = [t("ssl_title", domain), ""]
    try:
        ctx = ssl_lib.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                lines.append(t("ssl_subject", dict(x[0] for x in cert['subject']).get('commonName','N/A')))
                lines.append(t("ssl_issuer", dict(x[0] for x in cert['issuer']).get('commonName','N/A')))
                lines.append(t("ssl_valid_from", cert['notBefore']))
                lines.append(t("ssl_valid_to", cert['notAfter']))
                san = cert.get('subjectAltName', [])
                if san:
                    lines.append(t("ssl_san", ", ".join([x[1] for x in san[:5]])))
    except Exception as e:
        lines.append(t("ssl_error", str(e)))
    return "\n".join(lines), SOURCES_DB.get("ssl", [])