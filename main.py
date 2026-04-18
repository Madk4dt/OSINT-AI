# main.py (версия 13.97 – поддержка модов / mod support)
import sys
import re
import requests
import dns.resolver
from database import init_db, save_query, get_history, add_bookmark, list_bookmarks
from osint_modules import (
    email_lookup, username_search, domain_info, ip_info, phone_lookup, parse_website,
    scan_ports, subdomain_search, ssl_info, http_headers, github_search,
    extract_from_url, meta_file, banner_lookup, dns_recon, web_technologies,
    email_harvest, ip_range_scan, bgp_lookup, scan_single_port,
    analyze_security_headers, parse_sitemap, batch_scan, export_json, export_csv,
    analyze_js, compare_last_two, get_robots_txt, analyze_cookies, git_discovery,
    extract_comments, check_s3_bucket, save_session, load_session, legal_disclaimer
)
from utils import (
    t, set_language, print_header, print_success, print_error, print_info,
    print_table, print_result, check_internet, animated_print, c, print_banner,
    show_progress, print_warning, print_section, print_debug
)

# Импорты для модульной системы / Mod system imports
from core.loader import load_mods
from core.api import get_registered_commands

last_sources = []
last_query_type = None
last_query_value = None

# ------------------------------------------------------------
# Базовые команды (существующие) / Base commands (existing)
# ------------------------------------------------------------
COMMANDS = {
    r"^(?:search\s+)?email\s+(.+)": email_lookup,
    r"^(?:search\s+)?username\s+(.+)": username_search,
    r"^(?:search\s+)?domain\s+(.+)": domain_info,
    r"^(?:search\s+)?ip\s+(\d+\.\d+\.\d+\.\d+)": ip_info,
    r"^phone\s+(.+)$": phone_lookup,
    r"^parse\s+(.+?)(?:\s+(\d+))?$": "parse",
    r"^scanports\s+(.+)$": scan_ports,
    r"^subdomain\s+(.+)$": subdomain_search,
    r"^ssl\s+(.+)$": ssl_info,
    r"^httpheaders\s+(.+)$": http_headers,
    r"^github\s+(.+)$": github_search,
    r"^extract\s+(.+)$": extract_from_url,
    r"^meta\s+(.+)$": meta_file,
    r"^banner\s+(.+)$": banner_lookup,
    r"^dnsrecon\s+(.+)$": dns_recon,
    r"^webtech\s+(.+)$": web_technologies,
    r"^emailharvest\s+(.+)$": email_harvest,
    r"^iprange\s+(.+?)\s+(.+?)\s+(\d+)$": "iprange",
    r"^bgplookup\s+(.+)$": bgp_lookup,
    r"^history$": "history",
    r"^bookmark\s+(.+?)\s+(.+)": "bookmark",
    r"^list_bookmarks$": "list_bookmarks",
    r"^lang\s+(ru|en)$": "lang",
    r"^status$": "status",
    r"^myip$": "myip",
    r"^help(?:\s+(\S+))?$": "help",
    r"^exit$": "exit",
    r"^scanport\s+(\d+)\s+(.+)$": "scanport",
    r"^scan\s+port\s+(\d+)\s+(.+)$": "scanport",
    r"^secheaders\s+(.+)$": analyze_security_headers,
    r"^sitemap\s+(.+)$": parse_sitemap,
    r"^batch\s+(.+)$": "batch",
    r"^export_json(?:\s+(.+))?$": "export_json",
    r"^export_csv(?:\s+(.+))?$": "export_csv",
    r"^jsanalyze\s+(.+)$": analyze_js,
    r"^compare$": "compare",
    r"^robots\s+(.+)$": get_robots_txt,
    r"^cookies\s+(.+)$": analyze_cookies,
    r"^gitdiscovery\s+(.+)$": git_discovery,
    r"^comments\s+(.+)$": extract_comments,
    r"^s3check\s+(.+)$": check_s3_bucket,
    r"^session_save$": "session_save",
    r"^session_load$": "session_load",
    r"^legal$": "legal"
}

# ------------------------------------------------------------
# Обработка команд (та же логика, что и ранее)
# ------------------------------------------------------------
def process_command(user_input):
    global last_sources, last_query_type, last_query_value
    user_input = user_input.strip()
    if not user_input:
        return False

    if re.match(r"^(подробнее|расскажи|детали|more|details?)\s+(о\s+)?(.+)", user_input, re.I):
        if last_sources:
            show_sources(last_sources, last_query_type)
        else:
            print_info(t("no_sources_first"))
        return True

    low = user_input.lower()
    for pattern, handler in COMMANDS.items():
        m = re.match(pattern, low)
        if m:
            if callable(handler):
                arg = m.group(1)
                last_query_value = arg
                result, srcs = handler(arg)
                last_sources = srcs
                qtype = "search"
                for kw in ['email','username','domain','ip','phone','scanports','subdomain','ssl','httpheaders','github','extract','meta','banner','dnsrecon','webtech','emailharvest','bgplookup','secheaders','sitemap','jsanalyze','robots','cookies','gitdiscovery','comments','s3check']:
                    if kw in pattern:
                        qtype = kw
                        break
                save_query(qtype, arg, result[:500])
                print()
                if len(result) > 200:
                    print_result(result, title=f"{qtype.upper()}: {arg}", animate=True, title_color='cyan')
                else:
                    print_result(result, title=f"{qtype.upper()}: {arg}", animate=False, title_color='cyan')
                if srcs:
                    print("\n" + t("sources_additional"))
                    show_sources(srcs, qtype)
                return True

            elif handler == "parse":
                arg = m.group(1)
                depth = m.group(2) if m.group(2) else 1
                try:
                    depth = int(depth)
                except:
                    depth = 1
                result, srcs = parse_website(arg, depth)
                last_sources = srcs
                save_query("parse", arg, result[:500])
                print()
                print_result(result, title=f"PARSE: {arg}", animate=True, title_color='magenta')
                if srcs:
                    print("\n" + t("sources_additional"))
                    show_sources(srcs, "parse")
                return True

            elif handler == "iprange":
                start_ip = m.group(1)
                end_ip = m.group(2)
                port = m.group(3)
                result, srcs = ip_range_scan(start_ip, end_ip, port)
                last_sources = srcs
                save_query("iprange", f"{start_ip}-{end_ip}:{port}", result[:500])
                print()
                print_result(result, title=f"IPRANGE: {start_ip} – {end_ip} port {port}", title_color='yellow')
                if srcs:
                    print("\n" + t("sources_additional"))
                    show_sources(srcs, "iprange")
                return True

            elif handler == "scanport":
                port = m.group(1)
                host = m.group(2)
                result, srcs = scan_single_port(host, port)
                last_sources = srcs
                save_query("scanport", f"{host}:{port}", result[:500])
                print()
                print_result(result, title=f"SCANPORT: {host}:{port}", title_color='yellow')
                if srcs:
                    print("\n" + t("sources_additional"))
                    show_sources(srcs, "scanport")
                return True

            elif handler == "history":
                rows = get_history()
                if rows:
                    print_table(
                        ["Type", "Value", "Timestamp", "Result"],
                        [[r[0], r[1], r[2], r[3][:50]] for r in rows],
                        header_color='cyan'
                    )
                else:
                    print_info(t("history_empty"))
                return True

            elif handler == "bookmark":
                parts = user_input.split(maxsplit=2)
                if len(parts) >= 3:
                    add_bookmark(parts[1], parts[2])
                    print_success(t("bookmark_added", parts[1]))
                else:
                    print_error(t("bookmark_error"))
                return True

            elif handler == "list_bookmarks":
                bm = list_bookmarks()
                if bm:
                    print_table(["ID", "Title", "Timestamp"], bm, header_color='magenta')
                else:
                    print_info(t("bookmarks_empty"))
                return True

            elif handler == "lang":
                new = m.group(1)
                if set_language(new):
                    print_success(f"Language switched to {new}")
                else:
                    print_error(f"Unsupported: {new}")
                return True

            elif handler == "status":
                print_header("System Status", color='cyan')
                print(f"Internet:     {c('[+] OK', 'green') if check_internet() else c('[-] FAIL', 'red')}")
                try:
                    dns.resolver.resolve('google.com', 'A')
                    print(f"DNS:          {c('[+] OK', 'green')}")
                except:
                    print(f"DNS:          {c('[-] FAIL', 'red')}")
                try:
                    r = requests.get("https://emailrep.io/", timeout=5)
                    print(f"emailrep.io:  {c('[+] OK', 'green') if r.status_code == 200 else c('[-] '+str(r.status_code), 'red')}")
                except:
                    print(f"emailrep.io:  {c('[-] FAIL', 'red')}")
                try:
                    r = requests.get("http://ip-api.com/json/8.8.8.8", timeout=5)
                    if r.status_code == 200 and r.json().get('status') == 'success':
                        print(f"ip-api.com:   {c('[+] OK', 'green')}")
                    else:
                        print(f"ip-api.com:   {c('[-] FAIL', 'red')}")
                except:
                    print(f"ip-api.com:   {c('[-] FAIL', 'red')}")
                try:
                    import bs4
                    print(f"BeautifulSoup: {c('[+] OK', 'green')}")
                except:
                    print(f"BeautifulSoup: {c('[-] NOT INSTALLED', 'red')}")
                try:
                    import phonenumbers
                    print(f"phonenumbers:  {c('[+] OK', 'green')}")
                except:
                    print(f"phonenumbers:  {c('[-] NOT INSTALLED', 'red')}")
                try:
                    import exifread
                    print(f"exifread:      {c('[+] OK', 'green')}")
                except:
                    print(f"exifread:      {c('[-] NOT INSTALLED', 'red')}")
                try:
                    import PyPDF2
                    print(f"PyPDF2:        {c('[+] OK', 'green')}")
                except:
                    print(f"PyPDF2:        {c('[-] NOT INSTALLED', 'red')}")
                return True

            elif handler == "myip":
                try:
                    r = requests.get("https://api.ipify.org", timeout=10)
                    if r.status_code == 200:
                        real_ip = r.text.strip()
                        print_result(real_ip, title=t("myip_title"), animate=True, title_color='green')
                    else:
                        print_error(t("myip_error"))
                except:
                    print_error(t("myip_error"))
                return True

            elif handler == "help":
                cmd_arg = m.group(1)
                if cmd_arg:
                    help_key = f"help_{cmd_arg}"
                    help_text = t(help_key)
                    if help_text == help_key:
                        print_error(f"Нет справки для команды '{cmd_arg}'. Используйте 'help' для общего списка.")
                    else:
                        print_header(f"Справка: {cmd_arg}", color='cyan')
                        animated_print(help_text, delay=0.02, color='white')
                else:
                    # Основная справка (статическая)
                    print_header(t("help_header"), color='cyan')
                    animated_print(t("help_text"), delay=0.01, color='cyan')
                    # Добавляем команды модов, если есть
                    mod_commands = get_registered_commands()
                    if mod_commands:
                        print_section("МОДЫ / MOD COMMANDS", color='magenta')
                        for pattern in mod_commands.keys():
                            # Убираем regex-символы для красоты
                            cmd_display = pattern.replace(r'^', '').replace(r'$', '').replace(r'\s+', ' ').replace(r'\(.+\)', '<arg>')
                            print(f"  {c(cmd_display, 'green', bright=True)}")
                        print()
                return True

            elif handler == "exit":
                print_success(t("exit_msg"))
                sys.exit(0)

            elif handler == "batch":
                filename = m.group(1)
                result, _ = batch_scan(filename)
                print_result(result, title="BATCH SCAN")
                return True

            elif handler == "export_json":
                filename = m.group(1) if m.group(1) else None
                result, _ = export_json(filename)
                print_success(result)
                return True

            elif handler == "export_csv":
                filename = m.group(1) if m.group(1) else None
                result, _ = export_csv(filename)
                print_success(result)
                return True

            elif handler == "compare":
                result, _ = compare_last_two()
                print_result(result, title="COMPARE LAST TWO RESULTS")
                return True

            elif handler == "session_save":
                save_session()
                print_success("Сессия сохранена (история и закладки)")
                return True

            elif handler == "session_load":
                load_session()
                print_success("Сессия восстановлена")
                return True

            elif handler == "legal":
                result, _ = legal_disclaimer()
                print_result(result, title="LEGAL NOTICE")
                return True

    print_error(t("unknown_cmd"))
    return False

# ------------------------------------------------------------
# show_sources, print_detail (без изменений)
# ------------------------------------------------------------
def show_sources(sources, qtype):
    if not sources:
        print_info(t("sources_none"))
        return
    print("\n" + c(t("sources_prompt"), 'yellow', bright=True))
    for i, src in enumerate(sources, 1):
        print(f"  {c(str(i), 'yellow')}. {c(src['name'], 'cyan', bright=True)} — {src['description']}")
        print(f"     " + t("sources_method", src['method']) + "\n")
    while True:
        choice = input(c("\n" + t("sources_ask"), 'white')).strip()
        if choice.lower() in ['no', 'n', 'нет', '']:
            print_info(t("sources_ok"))
            return
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sources):
                src = sources[idx]
                print_detail(src, qtype)
                break
            else:
                print_error(t("sources_invalid"))
        else:
            found = next((s for s in sources if choice.lower() in s['name'].lower()), None)
            if found:
                print_detail(found, qtype)
                break
            else:
                print_error(t("sources_not_found"))

def print_detail(source, qtype):
    print_header(t("detail_header", source['name']), color='cyan')
    print(t("detail_info", source['description']))
    print(t("detail_method", source['method']))
    if source['name'] == "Sherlock":
        print("\n" + t("detail_example_sherlock"))
        print(f"   sherlock {last_query_value}")
    elif source['name'] == "crt.sh":
        print("\n" + t("detail_example_crtsh").format(last_query_value))
    elif source['name'] == "Hunter.io":
        print("\n" + t("detail_example_hunter"))
    elif source['name'] == "ip-api.com":
        print("\n" + t("detail_example_ipapi").format(last_query_value))
    elif source['name'] == "NumVerify":
        print("\n" + t("detail_example_numverify"))
    else:
        print("\n" + t("detail_general"))
    print()

# ------------------------------------------------------------
# Точка входа / Entry point
# ------------------------------------------------------------
def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    init_db()
    print_banner()
    animated_print(t("first_run_info"), delay=0.03, color='yellow')

    # ---------- ЗАГРУЗКА МОДОВ / LOAD MODS ----------
    print_info("Загрузка модов... / Loading mods...")
    loaded_mods = load_mods()
    if loaded_mods:
        print_success(f"Загружено модов: {len(loaded_mods)} / Loaded mods: {len(loaded_mods)}")
        mod_commands = get_registered_commands()
        for pattern, handler in mod_commands.items():
            if pattern in COMMANDS:
                print_warning(f"Команда {pattern} уже существует в ядре, мод переопределяет её / Command {pattern} already exists in core, mod overrides it")
            COMMANDS[pattern] = handler
            print_debug(f"Зарегистрирована команда мода: {pattern} / Registered mod command: {pattern}")
    else:
        print_info("Моды не найдены или не загружены / No mods found or loaded")
    # ------------------------------------------------

    # Вывод главного меню
    menu_lines = t("main_menu").split('\n')
    for line in menu_lines:
        if 'ПРОБИВ:' in line or 'LOOKUP:' in line:
            print(c("[LOOKUP] " + line, 'green', bright=True))
        elif 'СЕТЬ:' in line or 'NETWORK:' in line:
            print(c("[NETWORK] " + line, 'cyan', bright=True))
        elif 'ВЕБ:' in line or 'WEB:' in line:
            print(c("[WEB] " + line, 'magenta', bright=True))
        elif 'СИСТЕМА:' in line or 'SYSTEM:' in line:
            print(c("[SYSTEM] " + line, 'yellow', bright=True))
        else:
            print(line)

    # Отдельный блок с командами модов в меню
    mod_commands = get_registered_commands()
    if mod_commands:
        print_section("МОДЫ / MODS", color='magenta')
        for pattern in mod_commands.keys():
            cmd_display = pattern.replace(r'^', '').replace(r'$', '').replace(r'\s+', ' ').replace(r'\(.+\)', '<arg>')
            print(f"  {c(cmd_display, 'cyan', bright=True)}")
        print()

    while True:
        try:
            cmd = input(f"\n{c('>', 'cyan', bright=True)} ")
            process_command(cmd)
        except KeyboardInterrupt:
            print("\n")
            print_success(t("exit_msg"))
            sys.exit(0)
        except Exception as e:
            print_error(t("error_prefix", str(e)))

if __name__ == "__main__":
    main()
