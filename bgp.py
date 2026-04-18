# bgp.py
import socket
from utils import t, check_internet
from config import SOURCES_DB

def bgp_lookup(query):
    if not check_internet():
        return t("no_internet"), []
    lines = [f"BGP информация для {query}"]
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("whois.cymru.com", 43))
        if query.startswith("AS"):
            query = query[2:]
        if query.isdigit():
            sock.send(f" -v {query}\n".encode())
        else:
            sock.send(f" -v {query}\n".encode())
        data = sock.recv(4096).decode()
        sock.close()
        lines.append(data.strip())
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), SOURCES_DB.get("bgplookup", [])