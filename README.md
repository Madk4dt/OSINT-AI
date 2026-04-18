# 🔍 OSINT AI v13.97

**Professional OSINT Framework** — интеллектуальный сбор информации из открытых источников, сканирование сети, веб-анализ и модульная архитектура.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)

OSINT AI — мощная консольная утилита для OSINT, пентеста и кибербезопасности. Включает десятки модулей: от поиска email и username до сканирования портов, анализа SSL, парсинга сайтов и проверки безопасности заголовков. Поддерживает динамическую загрузку модов, экспорт отчётов, историю и мультиязычность.

> **Open Source · Modular · OSINT**

---

## 📚 Оглавление

- [✨ Ключевые возможности](#-ключевые-возможности)
- [⚙️ Установка](#️-установка)
- [📟 Команды](#-команды)
  - [🔍 Пробив информации](#-пробив-информации)
  - [🌐 Сеть и сканирование](#-сеть-и-сканирование)
  - [🕸️ Веб-анализ](#️-веб-анализ)
  - [⚙️ Системные команды](#️-системные-команды)
- [🧩 Разработка модов (Plugins)](#-разработка-модов-plugins)
  - [📁 Структура мода](#-структура-мода)
  - [📄 manifest.json](#-manifestjson)
  - [🔌 API для модов](#-api-для-модов)
  - [📝 Пример мода](#-пример-мода)
  - [🚀 Продвинутый пример](#-продвинутый-пример)
- [💡 Примеры использования](#-примеры-использования)
- [⚠️ Правовая информация](#️-правовая-информация)

---

## ✨ Ключевые возможности

- **🔎 Пробив информации:**  
  `email` (репутация, утечки, MX), `username` (300+ соцсетей), `domain` (WHOIS, A-записи), `ip` (геолокация, провайдер), `phone` (валидация).
- **🌐 Сканирование сети:**  
  сканер портов (500+), определение сервисов, баннеры, DNS-рекорды, BGP, iprange.
- **🕸️ Веб-анализ:**  
  парсинг, заголовки, технологии, безопасность (HSTS, CSP), robots.txt, sitemap, cookie, .git, JS-ключи, комментарии, S3.
- **🧩 Модульная система:**  
  подключаемые моды без перекомпиляции — просто положите мод в папку `mods/`.
- **📊 Отчёты:**  
  история, закладки, экспорт JSON/CSV, сравнение, сессии.

---

## ⚙️ Установка

Для установки OSINT AI клонируйте репозиторий и установите зависимости:

Сборка `.exe` (Windows):

```bash
pyinstaller --onefile --add-data "mods;mods" --add-data "core;core" main.py
```

---

## 📟 Команды

### 🔍 Пробив информации

| Команда | Описание | Пример |
|---------|----------|--------|
| `email <адрес>` | Репутация email, утечки, MX-записи | `email test@example.com` |
| `username <ник>` | Поиск профилей на 300+ сайтах | `username johndoe` |
| `domain <домен>` | WHOIS, A-записи, регистратор | `domain example.com` |
| `ip <IP>` | Геолокация, провайдер, координаты | `ip 8.8.8.8` |
| `phone <номер>` | Валидация, страна | `phone +79123456789` |
| `github <username>` | Информация о профиле GitHub | `github torvalds` |

### 🌐 Сеть и сканирование

| Команда | Описание | Пример |
|---------|----------|--------|
| `scanports <IP/домен>` | Сканирование 500+ портов с определением сервисов | `scanports 192.168.1.1` |
| `scanport <port> <IP>` | Проверка одного порта + баннер/HTTP | `scanport 443 google.com` |
| `subdomain <домен>` | Перебор популярных поддоменов | `subdomain example.com` |
| `ssl <домен>` | Информация об SSL-сертификате | `ssl github.com` |
| `dnsrecon <домен>` | Все DNS-записи (A, MX, TXT, NS, CNAME, SOA) | `dnsrecon google.com` |
| `bgplookup <IP/ASN>` | BGP-информация (whois.cymru.com) | `bgplookup 8.8.8.8` |
| `iprange <start> <end> <port>` | Сканирование диапазона IP на порт | `iprange 192.168.1.1 192.168.1.254 80` |
| `banner <IP> <port>` | Получение баннера сервиса | `banner 10.0.0.1 22` |

### 🕸️ Веб-анализ

| Команда | Описание | Пример |
|---------|----------|--------|
| `parse <url> [глубина]` | Сбор email, телефонов, username (с обходом ссылок) | `parse https://example.com 2` |
| `httpheaders <url>` | Показать HTTP-заголовки | `httpheaders https://kali.org` |
| `webtech <url>` | Определить технологии (CMS, JS-библиотеки) | `webtech https://wordpress.org` |
| `emailharvest <url>` | Извлечь все email со страницы | `emailharvest https://site.com/contacts` |
| `extract <url>` | Извлечь ссылки, формы, скрипты | `extract https://example.com` |
| `secheaders <url>` | Анализ заголовков безопасности (HSTS, CSP, X-Frame) | `secheaders https://paypal.com` |
| `sitemap <url>` | Парсинг sitemap.xml | `sitemap https://example.com` |
| `robots <url>` | Показать robots.txt | `robots https://google.com` |
| `cookies <url>` | Анализ cookie (Secure, HttpOnly, SameSite) | `cookies https://facebook.com` |
| `gitdiscovery <url>` | Поиск публичного .git/config | `gitdiscovery https://example.com` |
| `jsanalyze <url>` | Поиск API-ключей и email в JavaScript | `jsanalyze https://example.com/app.js` |
| `comments <url>` | Извлечение HTML-комментариев | `comments https://example.com` |
| `s3check <bucket>` | Проверка публичного S3-бакета на листинг | `s3check my-public-bucket` |

### ⚙️ Системные команды

| Команда | Описание |
|---------|----------|
| `myip` | Ваш реальный IP (без VPN) |
| `status` | Проверка интернета, DNS, зависимостей |
| `history` | Показать последние запросы |
| `bookmark <название> <текст>` | Сохранить закладку |
| `list_bookmarks` | Список закладок |
| `batch <файл>` | Выполнить команды из файла (построчно) |
| `export_json [файл]` | Экспорт истории в JSON |
| `export_csv [файл]` | Экспорт истории в CSV |
| `compare` | Сравнить два последних результата |
| `session_save` / `session_load` | Сохранить/восстановить сессию |
| `lang ru/en` | Смена языка |
| `help [команда]` | Справка |
| `legal` | Правовая информация |
| `exit` | Выход |

---

## 🧩 Разработка модов (Plugins)

OSINT AI имеет встроенную систему модов. Моды загружаются динамически из папки `mods/` без необходимости перекомпиляции. Это позволяет расширять функционал, добавлять новые команды и интеграции.

### 📁 Структура мода

Каждый мод — отдельная папка внутри `mods/`. Минимальный набор файлов:

```
mods/
└── my_cool_mod/
    ├── manifest.json       # метаданные
    └── main.py             # код мода (точка входа)
```

Файлы должны быть в кодировке **UTF-8**.

### 📄 manifest.json

```json
{
  "name": "My Cool Mod",
  "version": "1.0",
  "author": "Your Name",
  "description": "Добавляет команду mycmd",
  "commands": ["mycmd"]
}
```

### 🔌 API для модов

Мод получает доступ к безопасному API через аргументы функции `register()`. Доступные функции:

| Функция | Описание |
|---------|----------|
| `register_command(pattern, handler)` | Регистрирует новую команду. `pattern` — регулярное выражение, `handler` — функция, принимающая аргумент и возвращающая `(result_text, sources_list)`. |
| `print_success(msg)` | Вывод успешного сообщения (зелёный `[+]`). |
| `print_error(msg)` | Вывод ошибки (красный `[-]`). |
| `print_info(msg)` | Информационное сообщение (синий `[i]`). |
| `print_warning(msg)` | Предупреждение (жёлтый `[!]`). |
| `print_result(text, title=None, animate=False)` | Форматированный вывод результата. |
| `c(text, color, bright=False)` | Цветное оформление. |
| `t(key, *args)` | Локализация (поддержка мультиязычности). |
| `save_query(qtype, qvalue, result)` | Сохранить запрос в историю. |
| `get_history(limit=10)` | Получить историю. |
| `add_bookmark(title, content)` | Добавить закладку. |
| `is_valid_ip(ip)`, `is_valid_domain(domain)` | Валидация. |

Все эти функции импортируются из `core.api` и передаются в мод автоматически. Мод **не должен импортировать** что-либо кроме стандартной библиотеки Python.

### 📝 Пример мода (`main.py`)

```python
# mods/example_mod/main.py
def register(register_command, print_success, print_info):
    # Обработчик команды
    def my_cmd_handler(arg):
        # Здесь можно выполнять любые действия: http-запросы, вычисления и т.д.
        result = f"✨ Вы ввели: {arg}\nДлина аргумента: {len(arg)} символов."
        # Возвращаем (текст результата, список источников) — источники опциональны
        return result, []

    # Регистрируем команду с регулярным выражением
    register_command(r"^mycmd\s+(.+)$", my_cmd_handler)

    print_success("Example mod: команда 'mycmd' зарегистрирована")
    print_info("Используйте: mycmd <любой текст>")
```

После загрузки мода в программе появится команда `mycmd test`.

### 🚀 Продвинутый пример (с HTTP-запросом)

```python
def register(register_command, print_success, print_info, print_error):
    import requests

    def ip_info_handler(ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            if data.get('status') == 'success':
                result = f"IP: {ip}\nСтрана: {data['country']}\nГород: {data['city']}"
                return result, [{"name": "ip-api.com", "description": "геолокация"}]
            else:
                return "Ошибка геолокации", []
        except Exception as e:
            return f"Ошибка: {e}", []

    register_command(r"^myipinfo\s+(\d+\.\d+\.\d+\.\d+)$", ip_info_handler)
    print_success("Мод ipinfo загружен")
```

### 📌 Загрузка модов

При запуске OSINT AI сканирует папку `mods/` (сначала рядом с `.exe`, затем внутри сборки). Каждый валидный мод загружается, его команды добавляются в основной словарь. Если мод содержит ошибки, он пропускается с выводом сообщения в консоль.

> **Важно:** Моды **не имеют доступа** к внутренностям ядра (например, к глобальным переменным `last_sources`), что обеспечивает безопасность и стабильность.

---

## 💡 Примеры использования

### 1. Поиск username в соцсетях

```
> username security_researcher
[+] GitHub: https://github.com/security_researcher
[+] Twitter: https://twitter.com/security_researcher
[+] VK: https://vk.com/security_researcher
...
```

### 2. Сканирование портов веб-сервера

```
> scanports example.com
PORT     STATE    SERVICE         VERSION
22/tcp   open     SSH             OpenSSH 8.4
80/tcp   open     HTTP            nginx/1.20.2
443/tcp  open     HTTPS           nginx/1.20.2
3306/tcp closed   MySQL
...
```

### 3. Анализ безопасности сайта

```
> secheaders https://github.com
[+] Strict-Transport-Security: max-age=31536000
[+] Content-Security-Policy: default-src 'none'...
[+] X-Frame-Options: DENY
[!] CSP использует unsafe-inline (риск XSS)
```

### 4. Пакетное выполнение команд из файла

```
> batch targets.txt
Выполняется: email admin@example.com
Выполняется: scanports 10.0.0.1
...
```

---

## ⚠️ Правовая информация

Данный инструмент предназначен **ТОЛЬКО для авторизованного тестирования безопасности, OSINT-исследований и образовательных целей**. Вы должны иметь явное письменное разрешение на сканирование или сбор информации о любой цели, которой вы не владеете. Несанкционированный доступ к компьютерным системам является незаконным. Автор не несёт ответственности за неправомерное использование ПО.

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл [LICENSE](LICENSE).

---
