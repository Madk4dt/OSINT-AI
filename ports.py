# ports.py (версия 7.0 – улучшенный вывод, таймаут, протокольные пробы)
import socket
import concurrent.futures
import ssl as ssl_lib
import time
from utils import t, check_internet, is_valid_ip, is_valid_domain, show_progress, print_info, c
from config import SOURCES_DB

# Глобальная настройка таймаута (сек) – можно менять через команду
SCAN_TIMEOUT = 0.3

def set_scan_timeout(seconds):
    global SCAN_TIMEOUT
    SCAN_TIMEOUT = float(seconds)

# ------------------------------------------------------------
# Функция определения сервиса как в nmap (отправка проб и анализ ответа)
# ------------------------------------------------------------
def probe_service(host, port, timeout=3):
    """Отправляет протокол-специфичный запрос и возвращает название сервиса + версию."""
    service_name = "unknown"
    version = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        probes = {
            80: (b"GET / HTTP/1.0\r\nHost: " + host.encode() + b"\r\nUser-Agent: Nmap-Style\r\n\r\n", b"HTTP"),
            443: (b"HEAD / HTTP/1.0\r\n\r\n", b"HTTPS"),
            22: (b"SSH-2.0-Nmap-Scan\r\n", b"SSH"),
            21: (b"USER anonymous\r\n", b"FTP"),
            25: (b"EHLO test\r\n", b"SMTP"),
            110: (b"USER test\r\n", b"POP3"),
            143: (b"A001 CAPABILITY\r\n", b"IMAP"),
            3306: (b"\x00\x00\x00\x01\x01", b"MySQL"),
            5432: (b"\x00\x00\x00\x08\x04\xd2\x16\x2f", b"PostgreSQL"),
            6379: (b"PING\r\n", b"Redis"),
            27017: (b"\x3c\x00\x00\x00\xee\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"MongoDB"),
        }
        if port in probes:
            sock.send(probes[port][0])
            data = sock.recv(256).decode('utf-8', errors='ignore')
            service_name = probes[port][1]
            if service_name == "SSH" and "SSH-" in data:
                version = data.split()[0] if data.split() else ""
            elif service_name == "HTTP" and "Server:" in data:
                for line in data.split("\r\n"):
                    if line.lower().startswith("server:"):
                        version = line[7:].strip()
                        break
            elif service_name == "SMTP" and "220" in data:
                version = data.strip()[:50]
            elif service_name == "FTP" and "220" in data:
                version = data.strip()[:50]
            else:
                if data:
                    version = data[:50].replace('\n', ' ')
        else:
            sock.send(b"\n")
            data = sock.recv(256).decode('utf-8', errors='ignore')
            if data:
                version = data[:50].replace('\n', ' ')
        sock.close()
        return service_name, version
    except:
        return service_name, version

# ------------------------------------------------------------
# Функция получения HTTP-заголовков и тела
# ------------------------------------------------------------
def fetch_http_details(host, port, use_ssl=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        if use_ssl:
            context = ssl_lib.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        request = f"GET / HTTP/1.0\r\nHost: {host}\r\nUser-Agent: OSINT-Scanner\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if len(response) > 8192:
                response += b"\n... [truncated]"
                break
        sock.close()
        try:
            header_end = response.index(b"\r\n\r\n")
            headers = response[:header_end].decode('utf-8', errors='ignore')
            body = response[header_end+4:].decode('utf-8', errors='ignore')
        except ValueError:
            headers = response.decode('utf-8', errors='ignore')
            body = ""
        result = [c("\n--- HTTP Заголовки ---", 'cyan', bright=True), headers.strip()]
        if body.strip():
            result.append(c("--- Тело ответа (первые 8 КБ) ---", 'cyan', bright=True))
            body_preview = body[:2000] + ("..." if len(body) > 2000 else "")
            result.append(body_preview)
        return "\n".join(result)
    except Exception as e:
        return c(f"Ошибка HTTP: {str(e)}", 'red')

# ------------------------------------------------------------
# Сканирование всех портов с выводом в столбец
# ------------------------------------------------------------
def scan_ports(host):
    global SCAN_TIMEOUT
    if not check_internet():
        return t("no_internet"), []
    if not is_valid_ip(host) and not is_valid_domain(host):
        return t("invalid_ip") + " или " + t("invalid_domain"), []

    ports = [
        80,81,82,83,84,85,86,87,88,89,443,8443,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,
        25,26,465,587,110,995,143,993,2525,
        20,21,22,2222,23,
        1433,1434,3306,3307,5432,5433,27017,27018,6379,11211,9200,9300,5000,5001,
        3389,5900,5901,5902,5903,5800,5801,10000,
        53,67,68,69,123,161,162,389,636,3268,3269,5060,5061,
        1080,1081,3128,8000,8001,8008,8010,8118,8888,9000,9001,9043,9050,9051,9150,
        502,102,2404,44818,1883,8883,5683,5684,
        135,139,445,49152,49153,49154,49155,49156,49157,
        111,2049,4045,6000,6001,6002,6003,6004,6005,
        42,43,49,70,79,88,113,194,256,264,406,407,416,417,425,427,434,435,444,464,465,497,500,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600
    ]

    lines = [t("scanports_title", host), ""]
    open_ports = []
    all_results = []  # (port, is_open, service, version)

    total = len(ports)

    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SCAN_TIMEOUT)
        try:
            result = sock.connect_ex((host, port))
            is_open = (result == 0)
            if is_open:
                service, version = probe_service(host, port, timeout=2)
            else:
                service, version = "", ""
            return (port, is_open, service, version)
        except:
            return (port, False, "", "")
        finally:
            sock.close()

    print_info(f"Начинаю сканирование {total} портов (таймаут={SCAN_TIMEOUT}с)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = {executor.submit(check_port, port): port for port in ports}
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            port, is_open, service, version = future.result()
            completed += 1
            show_progress(completed, total, prefix="Сканирование портов", suffix=f" (порт {port})")
            all_results.append((port, is_open, service, version))
            if is_open:
                open_ports.append(port)

    # Вывод в столбцы (4 колонки)
    lines.append(c("\nPORT     STATE    SERVICE         VERSION", 'yellow', bright=True))
    lines.append(c("------   -----    -------         -------", 'white'))
    all_results.sort(key=lambda x: x[0])
    COLUMNS = 4
    rows = []
    for i in range(0, len(all_results), COLUMNS):
        row = []
        for j in range(COLUMNS):
            idx = i + j
            if idx < len(all_results):
                port, is_open, service, version = all_results[idx]
                status = c("open", 'green') if is_open else c("closed", 'red')
                serv_disp = service[:15] if service else ""
                vers_disp = version[:20] if version else ""
                row.append(f"{port:5} {status:7} {serv_disp:15} {vers_disp}")
            else:
                row.append("")
        rows.append(row)
    for row in rows:
        lines.append("  ".join(row))

    if not open_ports:
        lines.append("\n[i] Открытых портов не найдено. Возможно, хост за фаерволом.")
    else:
        lines.append(f"\n[+] Найдено открытых портов: {len(open_ports)}")

    # Анализ (краткий)
    lines.append("\n" + t("scanports_analysis"))
    if 22 in open_ports:
        lines.append("  [!] SSH доступен — возможен брутфорс, слабые ключи")
    if 3389 in open_ports:
        lines.append("  [!] RDP открыт — уязвимость BlueKeep")
    if 445 in open_ports:
        lines.append("  [!] SMB открыт — риск EternalBlue")
    if 3306 in open_ports:
        lines.append("  [!] MySQL открыт — слабые пароли")
    if 5432 in open_ports:
        lines.append("  [!] PostgreSQL — инъекции")
    if 27017 in open_ports:
        lines.append("  [!] MongoDB — без авторизации")
    if 6379 in open_ports:
        lines.append("  [!] Redis — риск RCE")
    if 11211 in open_ports:
        lines.append("  [!] Memcached — DDoS-усиление")
    if 5900 in open_ports:
        lines.append("  [!] VNC — уязвимости аутентификации")
    if 23 in open_ports:
        lines.append("  [!] Telnet — небезопасен")
    if 21 in open_ports:
        lines.append("  [!] FTP — анонимный доступ")
    if 25 in open_ports:
        lines.append("  [!] SMTP — открытый релей")

    lines.append("\n" + t("scanports_recommendations"))
    if len(open_ports) == len(ports):
        lines.append("  1. Отключите VPN, Tor или прокси.")
        lines.append("  2. Узнайте свой реальный IP (команда myip).")
        lines.append("  3. Повторите сканирование: scanports <реальный_IP>")
    else:
        lines.append(f"  • Детальное сканирование: nmap -sS -sV -p- -T4 {host}")
        if open_ports:
            lines.append(f"  • Проверка баннеров: banner {host} <порт>")
        lines.append(f"  • Поиск CVE для открытых сервисов через searchsploit")

    return "\n".join(lines), SOURCES_DB.get("scanports", [])

# ------------------------------------------------------------
# Сканирование одного порта с nmap-подобным определением
# ------------------------------------------------------------
def scan_single_port(host, port):
    global SCAN_TIMEOUT
    if not check_internet():
        return t("no_internet"), []
    if not is_valid_ip(host) and not is_valid_domain(host):
        return t("invalid_ip") + " или " + t("invalid_domain"), []
    try:
        port = int(port)
    except:
        return "Неверный номер порта", []

    lines = [f"Сканирование {host}:{port}", ""]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SCAN_TIMEOUT)
    try:
        start = time.time()
        result = sock.connect_ex((host, port))
        elapsed = time.time() - start
        if result == 0:
            lines.append(c(f"[+] Порт {port} открыт (время отклика {elapsed*1000:.2f} мс)", 'green', bright=True))
            service, version = probe_service(host, port, timeout=3)
            lines.append(c(f"Сервис: {service} {version}", 'cyan'))
            if port in [80, 443, 8080, 8443, 8000, 8888, 9000]:
                lines.append(c("\nПытаемся получить HTTP-заголовки и содержимое...", 'yellow'))
                is_https = port in [443, 8443, 9443]
                http_details = fetch_http_details(host, port, use_ssl=is_https)
                lines.append(http_details)
            else:
                try:
                    sock.send(b"\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        lines.append(c("Баннер сервиса:", 'cyan'))
                        lines.append(f"  {banner}")
                except:
                    pass
        else:
            lines.append(c(f"[-] Порт {port} закрыт (таймаут {SCAN_TIMEOUT}с)", 'red'))
    except Exception as e:
        lines.append(c(f"Ошибка: {e}", 'red'))
    finally:
        sock.close()
    return "\n".join(lines), SOURCES_DB.get("scanports", [])

# ------------------------------------------------------------
# Функции banner_lookup и ip_range_scan (восстановлены из старой версии)
# ------------------------------------------------------------
def get_banner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, int(port)))
        sock.send(b"\n")
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner
    except:
        return "Не удалось получить баннер"

def banner_lookup(host_port):
    parts = host_port.split()
    if len(parts) != 2:
        return "Использование: banner <IP> <порт>", []
    host, port = parts[0], parts[1]
    if not is_valid_ip(host) and not is_valid_domain(host):
        return t("invalid_ip") + " или " + t("invalid_domain"), []
    banner = get_banner(host, port)
    lines = [f"Баннер для {host}:{port}", banner]
    return "\n".join(lines), SOURCES_DB.get("banner", [])

def ip_range_scan(start_ip, end_ip, port):
    def ip_to_int(ip):
        parts = ip.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
    def int_to_ip(num):
        return f"{(num >> 24) & 0xFF}.{(num >> 16) & 0xFF}.{(num >> 8) & 0xFF}.{num & 0xFF}"
    try:
        start = ip_to_int(start_ip)
        end = ip_to_int(end_ip)
        port = int(port)
        lines = [f"Сканирование диапазона {start_ip} - {end_ip} на порт {port}"]
        open_hosts = []
        for ip_int in range(start, end+1):
            ip = int_to_ip(ip_int)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    lines.append(f"[+] {ip}:{port} открыт")
                    open_hosts.append(ip)
            except:
                pass
            finally:
                sock.close()
        if not open_hosts:
            lines.append("Открытых портов не найдено.")
        else:
            lines.append(f"\nНайдено {len(open_hosts)} хостов с открытым портом {port}")
    except Exception as e:
        lines.append(f"Ошибка: {e}")
    return "\n".join(lines), SOURCES_DB.get("iprange", [])