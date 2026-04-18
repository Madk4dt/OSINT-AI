# config.py
DB_PATH = "data/osint.db"

SOURCES_DB = {
    "email": [{"name": "emailrep.io", "description": "репутация email", "method": "API"}],
    "username": [{"name": "WhatsMyName", "description": "поиск по 300+ сайтам", "method": "HTTP"}],
    "domain": [{"name": "WHOIS", "description": "регистратор", "method": "whois"}],
    "ip": [{"name": "ip-api.com", "description": "геолокация", "method": "бесплатно"}],
    "phone": [{"name": "phonenumbers", "description": "валидация", "method": "локально"}],
    "parse": [{"name": "BeautifulSoup", "description": "парсинг", "method": "локально"}],
    "scanports": [{"name": "socket", "description": "сканирование портов", "method": "локально"}],
    "subdomain": [{"name": "DNS brute", "description": "перебор поддоменов", "method": "локально"}],
    "ssl": [{"name": "ssl module", "description": "сертификат", "method": "локально"}],
    "httpheaders": [{"name": "requests", "description": "заголовки", "method": "HTTP"}],
    "github": [{"name": "GitHub HTML", "description": "поиск пользователя", "method": "парсинг"}],
    "extract": [{"name": "BeautifulSoup", "description": "извлечение ссылок", "method": "локально"}],
    "meta": [{"name": "exifread", "description": "метаданные", "method": "локально"}],
    "banner": [{"name": "socket", "description": "баннер", "method": "сокет"}],
    "dnsrecon": [{"name": "dns.resolver", "description": "DNS записи", "method": "локально"}],
    "webtech": [{"name": "requests", "description": "технологии", "method": "HTTP"}],
    "emailharvest": [{"name": "regex", "description": "сбор email", "method": "регулярки"}],
    "iprange": [{"name": "socket", "description": "диапазон IP", "method": "сокеты"}],
    "bgplookup": [{"name": "whois.cymru.com", "description": "BGP", "method": "whois"}],
    "security_headers": [{"name": "requests", "description": "анализ заголовков безопасности", "method": "HTTP"}],
    "sitemap": [{"name": "sitemap.xml", "description": "парсинг карты сайта", "method": "XML"}],
    "robots": [{"name": "robots.txt", "description": "анализ правил роботов", "method": "HTTP"}],
    "cookies": [{"name": "requests", "description": "анализ cookie", "method": "HTTP"}],
    "git": [{"name": "git discovery", "description": "поиск .git/config", "method": "HTTP"}],
    "jsanalyzer": [{"name": "regex", "description": "поиск ключей в JS", "method": "локально"}],
    "comments": [{"name": "HTML comments", "description": "извлечение комментариев", "method": "локально"}],
    "s3": [{"name": "boto3", "description": "проверка S3 бакетов", "method": "HTTP"}],
    "batch": [{"name": "file", "description": "пакетное выполнение", "method": "локально"}],
    "export": [{"name": "JSON/CSV", "description": "экспорт отчётов", "method": "локально"}],
    "compare": [{"name": "diff", "description": "сравнение результатов", "method": "локально"}]
}

LANGUAGES = {
    "ru": {
        "email_title": "Результаты для email: {}",
        "email_reputation": "Репутация: {}",
        "email_breaches": "Утечки: {}",
        "email_mx": "MX-записи: {}",
        "email_error": "Ошибка: {}",
        "email_mx_error": "Не удалось получить MX для {}",
        "username_title": "Поиск username: {}",
        "username_found": "[+] {}: {}",
        "username_not_found": "[-] {}: не найден (код {})",
        "username_error": "[?] {}: ошибка",
        "username_none": "Профили не найдены.",
        "domain_title": "Анализ домена: {}",
        "domain_creation": "Создан: {}",
        "domain_expiration": "Истекает: {}",
        "domain_registrar": "Регистратор: {}",
        "domain_nameservers": "NS: {}",
        "domain_whois_error": "Ошибка WHOIS: {}",
        "domain_a_records": "A-записи: {}",
        "ip_title": "IP: {}",
        "ip_country": "Страна: {}",
        "ip_city": "Город: {}",
        "ip_isp": "Провайдер: {}",
        "ip_coords": "Координаты: {}, {}",
        "ip_error": "Ошибка: {}",
        "ip_api_error": "Ошибка ip-api: {}",
        "phone_title": "Номер: {}",
        "phone_country": "Страна: {}",
        "phone_valid": "Валидный: {}",
        "phone_operator": "Оператор: требуется API (NumVerify)",
        "phone_error": "Ошибка: {}",
        "invalid_phone": "Неверный формат (+79123456789)",
        "parse_title": "Парсинг: {}",
        "parse_emails": "Email:",
        "parse_phones": "Телефоны:",
        "parse_usernames": "Username:",
        "parse_links": "Обработано ссылок: {}",
        "parse_error": "Ошибка: {}",
        "scanports_title": "Сканирование портов {}",
        "scanports_open": "[+] Порт {} открыт",
        "scanports_closed": "[-] Порт {} закрыт",
        "scanports_analysis": "Анализ",
        "scanports_recommendations": "Рекомендации",
        "scanports_vpn_warning": "[!] Все порты открыты. Возможно, вы за VPN. Отключите и повторите.",
        "scanports_port_service": "Порт {} ({}) — {}",
        "scanports_advice_nmap": "nmap -sS -sV -p- {}",
        "scanports_advice_connect": "telnet {} {}",
        "scanports_advice_vuln": "Ищите CVE для открытых сервисов",
        "subdomain_title": "Поддомены {}",
        "subdomain_found": "[+] {}",
        "subdomain_not_found": "[-] {} не найден",
        "ssl_title": "SSL сертификат {}",
        "ssl_subject": "Субъект: {}",
        "ssl_issuer": "Издатель: {}",
        "ssl_valid_from": "С: {}",
        "ssl_valid_to": "До: {}",
        "ssl_san": "SubjectAltName: {}",
        "ssl_error": "Ошибка: {}",
        "httpheaders_title": "HTTP заголовки {}",
        "github_title": "GitHub: {}",
        "github_repos": "Репозитории: {}",
        "github_followers": "Подписчики: {}",
        "github_following": "Подписки: {}",
        "github_error": "Не найден",
        "extract_title": "Извлечение с {}",
        "extract_links": "Ссылки:",
        "extract_forms": "Формы:",
        "extract_scripts": "Скрипты:",
        "extract_error": "Ошибка: {}",
        "meta_title": "Метаданные {}",
        "meta_exif": "EXIF:",
        "meta_pdf": "PDF:",
        "meta_error": "Ошибка: {}",
        "myip_title": "Ваш реальный IP (без VPN)",
        "myip_error": "Не удалось определить",
        "banner_title": "Баннер для {}:{}",
        "dnsrecon_title": "DNS-записи для {}",
        "webtech_title": "Технологии сайта {}",
        "emailharvest_title": "Email с {}",
        "iprange_title": "Сканирование диапазона {} - {} на порт {}",
        "bgplookup_title": "BGP информация для {}",
        "sources_prompt": "Дополнительные источники:",
        "sources_method": "Метод: {}",
        "sources_ask": "Подробнее? (номер или название, 'нет'): ",
        "sources_invalid": "Неверно",
        "sources_not_found": "Не найдено",
        "sources_none": "Нет источников",
        "sources_ok": "Ок",
        "detail_header": "Детали: {}",
        "detail_info": "Описание: {}",
        "detail_method": "Как: {}",
        "detail_example_sherlock": "Установка: pip install sherlock-project",
        "detail_example_crtsh": "https://crt.sh/?q=%25.{}",
        "detail_example_hunter": "Регистрация на hunter.io",
        "detail_example_ipapi": "http://ip-api.com/json/{}",
        "detail_example_numverify": "https://numverify.com",
        "detail_general": "Поищите в интернете",
        "history_title": "История",
        "history_empty": "Пуста",
        "bookmark_added": "Закладка '{}' добавлена",
        "bookmark_error": "bookmark <название> <текст>",
        "bookmarks_empty": "Нет закладок",
        "help_header": "OSINT AI v13.97 - Команды",
        "help_text": """
\033[96m=== ПРОБИВ ИНФОРМАЦИИ ===\033[0m
email <адрес>      - репутация email, утечки, MX
username <ник>     - поиск профилей (GitHub, Twitter, Instagram и др.)
domain <домен>     - WHOIS, A-записи
ip <адрес>         - геолокация, провайдер
phone <номер>      - валидация, страна, оператор (требуется API)
github <username>  - данные профиля GitHub

\033[96m=== СКАНИРОВАНИЕ И СЕТЬ ===\033[0m
scanports <ip/домен>            - сканирование портов (500 штук)
scanport <port> <ip>            - сканирование порта
subdomain <домен>               - перебор поддоменов
ssl <домен>                     - SSL сертификат
dnsrecon <домен>                - все DNS записи (A, MX, TXT...)
bgplookup <IP/ASN>              - BGP информация
iprange <start> <end> <port>    - сканирование диапазона IP на порт
banner <IP> <порт>              - получение баннера

\033[96m=== ВЕБ-АНАЛИЗ ===\033[0m
parse <url> [глубина]      - сбор email, телефонов, username
httpheaders <url>          - HTTP заголовки
webtech <url>              - определение технологий сайта
emailharvest <url>         - сбор email со страницы
extract <url>              - извлечение ссылок, форм, скриптов
secheaders <url>           - анализ заголовков безопасности (HSTS, CSP)
sitemap <url>              - парсинг sitemap.xml
robots <url>               - показать robots.txt
cookies <url>              - анализ cookie безопасности
gitdiscovery <url>         - проверка .git/config
jsanalyze <url>            - поиск ключей и email в JS
comments <url>             - извлечение HTML-комментариев
s3check <bucket>           - проверка публичного S3 бакета

\033[96m=== СИСТЕМНЫЕ ===\033[0m
myip               - ваш реальный IP (без VPN)
status             - проверка соединения и зависимостей
history            - история запросов
bookmark <название> <содержание> - сохранить закладку
list_bookmarks     - список закладок
batch <файл>       - выполнить команды из файла
export_json [файл] - экспорт истории в JSON
export_csv [файл]  - экспорт истории в CSV
compare            - сравнить два последних результата
session_save       - сохранить сессию
session_load       - загрузить сессию
lang <ru/en>       - смена языка
help               - эта справка
legal              - правовая информация
exit               - выход
""",
        "help_ip": "IP-адрес - геолокация, провайдер, координаты.\nСинтаксис: ip <IP>\nПример: ip 8.8.8.8",
        "help_email": "Email - репутация, утечки, MX-записи.\nСинтаксис: email <адрес>\nПример: email test@example.com",
        "help_username": "Username - поиск профилей в соцсетях.\nСинтаксис: username <ник>\nПример: username john_doe",
        "help_domain": "Домен - WHOIS, A-записи, регистратор.\nСинтаксис: domain <домен>\nПример: domain example.com",
        "help_phone": "Телефон - валидация, страна.\nСинтаксис: phone <номер>\nПример: phone +79123456789",
        "help_github": "GitHub - информация о пользователе.\nСинтаксис: github <username>\nПример: github torvalds",
        "help_scanports": "Сканирование портов - проверка открытых портов.\nСинтаксис: scanports <IP/домен>\nПример: scanports 192.168.1.1",
        "help_subdomain": "Поиск поддоменов - перебор популярных поддоменов.\nСинтаксис: subdomain <домен>\nПример: subdomain example.com",
        "help_ssl": "SSL сертификат - информация о сертификате.\nСинтаксис: ssl <домен>\nПример: ssl google.com",
        "help_dnsrecon": "DNS записи - все типы записей.\nСинтаксис: dnsrecon <домен>\nПример: dnsrecon example.com",
        "help_bgplookup": "BGP информация - автономная система.\nСинтаксис: bgplookup <IP/ASN>\nПример: bgplookup 8.8.8.8",
        "help_iprange": "Сканирование диапазона IP - проверка порта на диапазоне.\nСинтаксис: iprange <start> <end> <port>\nПример: iprange 192.168.1.1 192.168.1.254 80",
        "help_banner": "Баннер сервиса - получение баннера.\nСинтаксис: banner <IP> <порт>\nПример: banner 192.168.1.1 22",
        "help_parse": "Парсинг сайта - сбор email, телефонов, username.\nСинтаксис: parse <url> [глубина]\nПример: parse https://example.com 2",
        "help_httpheaders": "HTTP заголовки - анализ заголовков ответа.\nСинтаксис: httpheaders <url>\nПример: httpheaders https://example.com",
        "help_webtech": "Технологии сайта - определение CMS, JS библиотек.\nСинтаксис: webtech <url>\nПример: webtech https://example.com",
        "help_emailharvest": "Сбор email - извлечение email со страницы.\nСинтаксис: emailharvest <url>\nПример: emailharvest https://example.com",
        "help_extract": "Извлечение ссылок, форм, скриптов.\nСинтаксис: extract <url>\nПример: extract https://example.com",
        "help_meta": "Метаданные файла - EXIF, PDF.\nСинтаксис: meta <путь к файлу>\nПример: meta image.jpg",
        "help_myip": "Ваш реальный IP без VPN.\nСинтаксис: myip",
        "help_status": "Проверка соединения и зависимостей.\nСинтаксис: status",
        "help_history": "История запросов.\nСинтаксис: history",
        "help_bookmark": "Сохранить закладку.\nСинтаксис: bookmark <название> <содержание>\nПример: bookmark google 8.8.8.8",
        "help_list_bookmarks": "Показать закладки.\nСинтаксис: list_bookmarks",
        "help_lang": "Сменить язык.\nСинтаксис: lang <ru/en>",
        "help_exit": "Выйти из программы.\nСинтаксис: exit",
        "help_secheaders": "Анализ заголовков безопасности (HSTS, CSP, X-Frame-Options).\nСинтаксис: secheaders <url>",
        "help_sitemap": "Парсинг sitemap.xml.\nСинтаксис: sitemap <url>",
        "help_batch": "Пакетное выполнение команд из файла (построчно).\nСинтаксис: batch <файл>",
        "help_export_json": "Экспорт истории запросов в JSON.\nСинтаксис: export_json [имя_файла]",
        "help_export_csv": "Экспорт истории запросов в CSV.\nСинтаксис: export_csv [имя_файла]",
        "help_jsanalyze": "Анализ JavaScript на предмет API ключей и email.\nСинтаксис: jsanalyze <url>",
        "help_compare": "Сравнить два последних результата из истории.\nСинтаксис: compare",
        "help_robots": "Показать содержимое robots.txt.\nСинтаксис: robots <url>",
        "help_cookies": "Анализ безопасности cookie (Secure, HttpOnly, SameSite).\nСинтаксис: cookies <url>",
        "help_git": "Проверка наличия публичного .git/config.\nСинтаксис: gitdiscovery <url>",
        "help_comments": "Извлечение HTML-комментариев (могут содержать логины, пути).\nСинтаксис: comments <url>",
        "help_s3": "Проверка публичного S3 бакета на листинг.\nСинтаксис: s3check <bucket-name>",
        "help_session_save": "Сохранить текущую сессию (историю и закладки) в файл.\nСинтаксис: session_save",
        "help_session_load": "Загрузить сессию из файла.\nСинтаксис: session_load",
        "help_legal": "Показать правовую информацию об этичном использовании.\nСинтаксис: legal",
        "main_menu": "\n\033[96m=== ОСНОВНОЕ МЕНЮ v13.97 ===\033[0m\n\033[93mПРОБИВ:\033[0m email, username, domain, ip, phone, github\n\033[93mСЕТЬ:\033[0m scanports, subdomain, ssl, dnsrecon, bgplookup, iprange, banner\n\033[93mВЕБ:\033[0m parse, httpheaders, webtech, emailharvest, extract, secheaders, sitemap, robots, cookies, gitdiscovery, jsanalyze, comments, s3check\n\033[93mСИСТЕМА:\033[0m myip, status, history, bookmark, list_bookmarks, batch, export_json, export_csv, compare, session_save, session_load, lang, help, legal, exit",
        "unknown_cmd": "Неизвестная команда. help",
        "exit_msg": "До свидания",
        "first_run_info": "OSINT AI v13.97. Язык русский. lang en для английского.",
        "sources_additional": "Дополнительные источники:",
        "no_sources_first": "Сначала выполните поиск",
        "error_prefix": "Ошибка: {}",
        "no_internet": "Нет интернета",
        "invalid_email": "Неверный email",
        "invalid_username": "Неверный username (2-30 букв, цифр, _, -)",
        "invalid_domain": "Неверный домен",
        "invalid_ip": "Неверный IP",
        "invalid_url": "Неверный URL",
        "invalid_file": "Файл не найден",
        "timeout_error": "Таймаут"
    },
    "en": {
        "email_title": "Results for email: {}",
        "email_reputation": "Reputation: {}",
        "email_breaches": "Breaches: {}",
        "email_mx": "MX records: {}",
        "email_error": "Error: {}",
        "email_mx_error": "Could not retrieve MX for {}",
        "username_title": "Username search: {}",
        "username_found": "[+] {}: {}",
        "username_not_found": "[-] {}: not found (code {})",
        "username_error": "[?] {}: error",
        "username_none": "No profiles found.",
        "domain_title": "Domain analysis: {}",
        "domain_creation": "Creation: {}",
        "domain_expiration": "Expiration: {}",
        "domain_registrar": "Registrar: {}",
        "domain_nameservers": "NS: {}",
        "domain_whois_error": "WHOIS error: {}",
        "domain_a_records": "A records: {}",
        "ip_title": "IP: {}",
        "ip_country": "Country: {}",
        "ip_city": "City: {}",
        "ip_isp": "ISP: {}",
        "ip_coords": "Coordinates: {}, {}",
        "ip_error": "Error: {}",
        "ip_api_error": "ip-api error: {}",
        "phone_title": "Phone: {}",
        "phone_country": "Country: {}",
        "phone_valid": "Valid: {}",
        "phone_operator": "Carrier: API required (NumVerify)",
        "phone_error": "Error: {}",
        "invalid_phone": "Invalid format (+79123456789)",
        "parse_title": "Parsing: {}",
        "parse_emails": "Emails:",
        "parse_phones": "Phones:",
        "parse_usernames": "Usernames:",
        "parse_links": "Links processed: {}",
        "parse_error": "Error: {}",
        "scanports_title": "Port scanning {}",
        "scanports_open": "[+] Port {} open",
        "scanports_closed": "[-] Port {} closed",
        "scanports_analysis": "Analysis",
        "scanports_recommendations": "Recommendations",
        "scanports_vpn_warning": "[!] All ports open. Are you behind VPN? Disable and retry.",
        "scanports_port_service": "Port {} ({}) — {}",
        "scanports_advice_nmap": "nmap -sS -sV -p- {}",
        "scanports_advice_connect": "telnet {} {}",
        "scanports_advice_vuln": "Search CVE for open services",
        "subdomain_title": "Subdomains of {}",
        "subdomain_found": "[+] {}",
        "subdomain_not_found": "[-] {} not found",
        "ssl_title": "SSL certificate {}",
        "ssl_subject": "Subject: {}",
        "ssl_issuer": "Issuer: {}",
        "ssl_valid_from": "From: {}",
        "ssl_valid_to": "To: {}",
        "ssl_san": "SubjectAltName: {}",
        "ssl_error": "Error: {}",
        "httpheaders_title": "HTTP headers of {}",
        "github_title": "GitHub: {}",
        "github_repos": "Repos: {}",
        "github_followers": "Followers: {}",
        "github_following": "Following: {}",
        "github_error": "Not found",
        "extract_title": "Extracted from {}",
        "extract_links": "Links:",
        "extract_forms": "Forms:",
        "extract_scripts": "Scripts:",
        "extract_error": "Error: {}",
        "meta_title": "Metadata of {}",
        "meta_exif": "EXIF:",
        "meta_pdf": "PDF:",
        "meta_error": "Error: {}",
        "myip_title": "Your real IP (no VPN)",
        "myip_error": "Could not determine",
        "banner_title": "Banner for {}:{}",
        "dnsrecon_title": "DNS records for {}",
        "webtech_title": "Technologies of {}",
        "emailharvest_title": "Emails from {}",
        "iprange_title": "Scanning range {} - {} port {}",
        "bgplookup_title": "BGP info for {}",
        "sources_prompt": "Additional sources:",
        "sources_method": "Method: {}",
        "sources_ask": "More details? (number or name, 'no'): ",
        "sources_invalid": "Invalid",
        "sources_not_found": "Not found",
        "sources_none": "No sources",
        "sources_ok": "OK",
        "detail_header": "Details: {}",
        "detail_info": "Info: {}",
        "detail_method": "How: {}",
        "detail_example_sherlock": "Install: pip install sherlock-project",
        "detail_example_crtsh": "https://crt.sh/?q=%25.{}",
        "detail_example_hunter": "Register at hunter.io",
        "detail_example_ipapi": "http://ip-api.com/json/{}",
        "detail_example_numverify": "https://numverify.com",
        "detail_general": "Search online",
        "history_title": "History",
        "history_empty": "Empty",
        "bookmark_added": "Bookmark '{}' added",
        "bookmark_error": "bookmark <title> <content>",
        "bookmarks_empty": "No bookmarks",
        "help_header": "OSINT AI v13.97 - Commands",
        "help_text": """
\033[96m=== INFORMATION LOOKUP ===\033[0m
email <address>      - email reputation, breaches, MX
username <nick>      - social media search (GitHub, Twitter, Instagram etc.)
domain <domain>      - WHOIS, A records
ip <address>         - geolocation, ISP
phone <number>       - validation, country, carrier (API required)
github <username>    - GitHub profile data

\033[96m=== SCANNING & NETWORK ===\033[0m
scanports <ip/domain>           - port scanning (500 common ports)
scanport <port> <ip>            - single port scan
subdomain <domain>              - subdomain brute force
ssl <domain>                    - SSL certificate info
dnsrecon <domain>               - all DNS records (A, MX, TXT...)
bgplookup <IP/ASN>              - BGP information
iprange <start> <end> <port>    - scan IP range for a port
banner <IP> <port>              - grab service banner

\033[96m=== WEB ANALYSIS ===\033[0m
parse <url> [depth]      - extract emails, phones, usernames
httpheaders <url>        - HTTP headers
webtech <url>            - detect website technologies
emailharvest <url>       - collect emails from page
extract <url>            - extract links, forms, scripts
secheaders <url>         - analyze security headers (HSTS, CSP)
sitemap <url>            - parse sitemap.xml
robots <url>             - show robots.txt
cookies <url>            - analyze cookie security
gitdiscovery <url>       - check for .git/config
jsanalyze <url>          - find API keys and emails in JS
comments <url>           - extract HTML comments
s3check <bucket>         - check public S3 bucket listing

\033[96m=== SYSTEM ===\033[0m
myip               - your real IP (no VPN)
status             - check internet and dependencies
history            - query history
bookmark <title> <content> - save a bookmark
list_bookmarks     - show bookmarks
batch <file>       - run commands from file
export_json [file] - export history to JSON
export_csv [file]  - export history to CSV
compare            - compare last two results
session_save       - save session (history & bookmarks)
session_load       - load session
lang <ru/en>       - change language
help               - this help
legal              - legal disclaimer
exit               - exit
""",
        "help_ip": "IP address - geolocation, ISP, coordinates.\nSyntax: ip <IP>\nExample: ip 8.8.8.8",
        "help_email": "Email - reputation, breaches, MX records.\nSyntax: email <address>\nExample: email test@example.com",
        "help_username": "Username - search profiles on social networks.\nSyntax: username <nick>\nExample: username john_doe",
        "help_domain": "Domain - WHOIS, A records, registrar.\nSyntax: domain <domain>\nExample: domain example.com",
        "help_phone": "Phone - validation, country.\nSyntax: phone <number>\nExample: phone +79123456789",
        "help_github": "GitHub - user information.\nSyntax: github <username>\nExample: github torvalds",
        "help_scanports": "Port scanning - check open ports.\nSyntax: scanports <IP/domain>\nExample: scanports 192.168.1.1",
        "help_subdomain": "Subdomain search - brute force common subdomains.\nSyntax: subdomain <domain>\nExample: subdomain example.com",
        "help_ssl": "SSL certificate - certificate information.\nSyntax: ssl <domain>\nExample: ssl google.com",
        "help_dnsrecon": "DNS records - all record types.\nSyntax: dnsrecon <domain>\nExample: dnsrecon example.com",
        "help_bgplookup": "BGP information - autonomous system.\nSyntax: bgplookup <IP/ASN>\nExample: bgplookup 8.8.8.8",
        "help_iprange": "IP range scan - check a port on a range.\nSyntax: iprange <start> <end> <port>\nExample: iprange 192.168.1.1 192.168.1.254 80",
        "help_banner": "Service banner - grab banner.\nSyntax: banner <IP> <port>\nExample: banner 192.168.1.1 22",
        "help_parse": "Website parsing - collect emails, phones, usernames.\nSyntax: parse <url> [depth]\nExample: parse https://example.com 2",
        "help_httpheaders": "HTTP headers - analyze response headers.\nSyntax: httpheaders <url>\nExample: httpheaders https://example.com",
        "help_webtech": "Website technologies - detect CMS, JS libraries.\nSyntax: webtech <url>\nExample: webtech https://example.com",
        "help_emailharvest": "Email harvest - extract emails from page.\nSyntax: emailharvest <url>\nExample: emailharvest https://example.com",
        "help_extract": "Extract links, forms, scripts.\nSyntax: extract <url>\nExample: extract https://example.com",
        "help_meta": "File metadata - EXIF, PDF.\nSyntax: meta <filepath>\nExample: meta image.jpg",
        "help_myip": "Your real IP without VPN.\nSyntax: myip",
        "help_status": "Check internet and dependencies.\nSyntax: status",
        "help_history": "Query history.\nSyntax: history",
        "help_bookmark": "Save a bookmark.\nSyntax: bookmark <title> <content>\nExample: bookmark google 8.8.8.8",
        "help_list_bookmarks": "Show bookmarks.\nSyntax: list_bookmarks",
        "help_lang": "Change language.\nSyntax: lang <ru/en>",
        "help_exit": "Exit the program.\nSyntax: exit",
        "help_secheaders": "Analyze security headers (HSTS, CSP, X-Frame-Options).\nSyntax: secheaders <url>",
        "help_sitemap": "Parse sitemap.xml.\nSyntax: sitemap <url>",
        "help_batch": "Batch execute commands from a file (one per line).\nSyntax: batch <file>",
        "help_export_json": "Export query history to JSON.\nSyntax: export_json [filename]",
        "help_export_csv": "Export query history to CSV.\nSyntax: export_csv [filename]",
        "help_jsanalyze": "Analyze JavaScript for API keys and emails.\nSyntax: jsanalyze <url>",
        "help_compare": "Compare the last two results in history.\nSyntax: compare",
        "help_robots": "Show robots.txt content.\nSyntax: robots <url>",
        "help_cookies": "Analyze cookie security (Secure, HttpOnly, SameSite).\nSyntax: cookies <url>",
        "help_git": "Check for public .git/config.\nSyntax: gitdiscovery <url>",
        "help_comments": "Extract HTML comments (may contain logins, paths).\nSyntax: comments <url>",
        "help_s3": "Check public S3 bucket for listing.\nSyntax: s3check <bucket-name>",
        "help_session_save": "Save current session (history and bookmarks) to file.\nSyntax: session_save",
        "help_session_load": "Load session from file.\nSyntax: session_load",
        "help_legal": "Show legal information about ethical use.\nSyntax: legal",
        "main_menu": "\n\033[96m=== MAIN MENU v13.97 ===\033[0m\n\033[93mLOOKUP:\033[0m email, username, domain, ip, phone, github\n\033[93mNETWORK:\033[0m scanports, subdomain, ssl, dnsrecon, bgplookup, iprange, banner\n\033[93mWEB:\033[0m parse, httpheaders, webtech, emailharvest, extract, secheaders, sitemap, robots, cookies, gitdiscovery, jsanalyze, comments, s3check\n\033[93mSYSTEM:\033[0m myip, status, history, bookmark, list_bookmarks, batch, export_json, export_csv, compare, session_save, session_load, lang, help, legal, exit",
        "unknown_cmd": "Unknown command. help",
        "exit_msg": "Goodbye",
        "first_run_info": "OSINT AI v13.97. Language English. lang ru for Russian.",
        "sources_additional": "Additional sources:",
        "no_sources_first": "Run a search first",
        "error_prefix": "Error: {}",
        "no_internet": "No internet",
        "invalid_email": "Invalid email",
        "invalid_username": "Invalid username (2-30 letters, digits, _, -)",
        "invalid_domain": "Invalid domain",
        "invalid_ip": "Invalid IP",
        "invalid_url": "Invalid URL",
        "invalid_file": "File not found",
        "timeout_error": "Timeout"
    }
}

CURRENT_LANG = "ru"
