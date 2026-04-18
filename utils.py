# utils.py (версия 13.97 – полная)
# Модуль вспомогательных функций: цвета, интернационализация, валидация, анимация, прогресс, баннер и пр.

import sys
import socket
import re
import time
import phonenumbers
from config import LANGUAGES, CURRENT_LANG

# Попытка импорта colorama для цветного вывода в консоли Windows
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True, convert=True)
    COLORS = True
except ImportError:
    COLORS = False
    # Заглушки для цветов, если colorama не установлена
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = BLACK = BLUE = ''
    class Back:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = BLACK = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''

# Дополнительные 256-цветные коды ANSI (для особых цветов)
COLORS_256 = {
    'orange': '\033[38;5;208m',
    'lime': '\033[38;5;118m',
    'pink': '\033[38;5;213m',
    'teal': '\033[38;5;37m',
    'purple': '\033[38;5;129m',
    'gold': '\033[38;5;220m',
    'silver': '\033[38;5;250m',
    'coral': '\033[38;5;209m',
}

# ------------------------------------------------------------
# Интернационализация (i18n)
# ------------------------------------------------------------
def t(key, *args):
    """Возвращает локализованную строку по ключу с подстановкой аргументов."""
    global CURRENT_LANG
    lang_dict = LANGUAGES.get(CURRENT_LANG, LANGUAGES["ru"])
    text = lang_dict.get(key, key)
    if args:
        return text.format(*args)
    return text

def set_language(lang):
    """Устанавливает текущий язык (ru/en). Возвращает True при успехе."""
    global CURRENT_LANG
    if lang in LANGUAGES:
        CURRENT_LANG = lang
        return True
    return False

# ------------------------------------------------------------
# Валидация входных данных
# ------------------------------------------------------------
def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

def is_valid_username(username):
    return 2 <= len(username) <= 30 and re.match(r'^[a-zA-Z0-9_.-]+$', username) is not None

def is_valid_domain(domain):
    return re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', domain) is not None

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

def is_valid_phone(phone):
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(phone, None))
    except:
        return False

def is_valid_url(url):
    return url.startswith(('http://', 'https://'))

def check_internet():
    """Проверяет доступ в интернет через DNS запрос к 8.8.8.8:53."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# ------------------------------------------------------------
# Центральная функция форматирования с цветом
# ------------------------------------------------------------
def c(text, color=None, bright=False, underline=False, blink=False, bg=None, hex_color=None):
    """
    Оборачивает текст ANSI-кодами цвета.
    Параметры:
        text: строка
        color: название цвета (red, green, yellow, cyan, magenta, white, black, blue)
               или из COLORS_256 (orange, lime, pink, teal, purple, gold, silver, coral)
        bright: яркий текст
        underline: подчёркивание
        blink: мигание (редко где работает)
        bg: цвет фона (red, green, ...)
        hex_color: кортеж (r,g,b) или строка вида '#RRGGBB'
    """
    if not COLORS:
        return text
    codes = []
    if bright:
        codes.append(Style.BRIGHT)
    if underline:
        codes.append('\033[4m')
    if blink:
        codes.append('\033[5m')
    if bg:
        bg_code = getattr(Back, bg.upper(), '')
        if bg_code:
            codes.append(bg_code)
    if hex_color:
        if isinstance(hex_color, tuple):
            codes.append(rgb(*hex_color))
        elif isinstance(hex_color, str) and hex_color.startswith('#'):
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            codes.append(rgb(r, g, b))
    elif color:
        color_code = getattr(Fore, color.upper(), '')
        if color_code:
            codes.append(color_code)
        elif color in COLORS_256:
            codes.append(COLORS_256[color])
    if codes:
        return ''.join(codes) + text + Style.RESET_ALL
    return text

def rgb(r, g, b):
    """Возвращает ANSI код для 24-битного цвета."""
    if not COLORS:
        return ''
    return f'\033[38;2;{r};{g};{b}m'

def bg_rgb(r, g, b):
    """Возвращает ANSI код для 24-битного цвета фона."""
    if not COLORS:
        return ''
    return f'\033[48;2;{r};{g};{b}m'

# ------------------------------------------------------------
# Улучшенные функции вывода
# ------------------------------------------------------------
def print_header(title, color='cyan'):
    """Печатает заголовок с рамкой."""
    line = c('═' * (len(title) + 4), color, bright=True)
    print(f"\n{line}")
    print(f"{c('>>', color)}  {c(title.upper(), color, bright=True, underline=True)}")
    print(line)

def print_success(msg):
    print(f"{c('[+]', 'green', bright=True)} {c(msg, 'green')}")

def print_error(msg):
    print(f"{c('[-]', 'red', bright=True)} {c(msg, 'red')}")

def print_info(msg):
    print(f"{c('[i]', 'cyan', bright=True)} {c(msg, 'cyan')}")

def print_warning(msg):
    print(f"{c('[!]', 'yellow', bright=True)} {c(msg, 'yellow', bright=True)}")

def print_debug(msg):
    """Отладочное сообщение (обычно для модов)."""
    print(f"{c('[=]', 'magenta')} {c(msg, 'magenta')}")

def print_section(title, char='─', color='magenta'):
    """Печатает раздел с линией."""
    line = c(char * (len(title) + 4), color)
    print(f"\n{line}")
    print(f"{c('┤', color)} {c(title, color, bright=True)} {c('├', color)}")
    print(line)

def print_key_value(key, value, indent=0, key_color='white', value_color='yellow'):
    spaces = "  " * indent
    print(f"{spaces}{c(key, key_color, bright=True)}: {c(str(value), value_color)}")

def print_list(items, indent=1, marker="•", marker_color='cyan'):
    spaces = "  " * indent
    for item in items:
        print(f"{spaces}{c(marker, marker_color)} {item}")

def print_table(headers, rows, border=True, header_color='cyan', row_colors=None):
    """
    Печатает таблицу с выравниванием.
    headers: список заголовков
    rows: список списков строк
    border: рисовать границы
    header_color: цвет заголовков
    row_colors: список цветов для чередования строк
    """
    if not rows:
        return
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    if border:
        top = "┌" + "┬".join(c("─" * (w + 2), 'white') for w in col_widths) + "┐"
        print(top)
    header_line = "│ " + " │ ".join(c(str(h).ljust(col_widths[i]), header_color, bright=True, underline=True) for i, h in enumerate(headers)) + " │"
    print(header_line)
    if border:
        sep = "├" + "┼".join(c("─" * (w + 2), 'white') for w in col_widths) + "┤"
        print(sep)
    for idx, row in enumerate(rows):
        row_color = row_colors[idx % len(row_colors)] if row_colors else None
        line = "│ " + " │ ".join(c(str(cell).ljust(col_widths[i]), row_color) for i, cell in enumerate(row)) + " │"
        print(line)
    if border:
        bottom = "└" + "┴".join(c("─" * (w + 2), 'white') for w in col_widths) + "┘"
        print(bottom)

def animated_print(text, delay=0.02, color=None, bright=False, end='\n'):
    """
    Печатает текст с эффектом печати на машинке (побуквенно).
    Поддерживает ANSI-последовательности (цвета не разбиваются).
    """
    if color or bright:
        styled_text = c(text, color, bright)
    else:
        styled_text = text
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*m')
    parts = []
    idx = 0
    for match in ansi_pattern.finditer(styled_text):
        if idx < match.start():
            parts.append(styled_text[idx:match.start()])
        parts.append(match.group())
        idx = match.end()
    if idx < len(styled_text):
        parts.append(styled_text[idx:])
    for part in parts:
        if part.startswith('\x1b['):
            sys.stdout.write(part)
            sys.stdout.flush()
        else:
            for ch in part:
                sys.stdout.write(ch)
                sys.stdout.flush()
                time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def show_progress(current, total, prefix="", suffix="", bar_length=50, show_percent=True):
    """
    Отображает прогресс-бар в консоли.
    current: текущее значение
    total: общее значение
    prefix: текст перед баром
    suffix: текст после бара
    bar_length: длина бара в символах
    show_percent: показывать проценты
    """
    percent = 100 * (current / float(total))
    filled_len = int(bar_length * current // total)
    if percent < 50:
        bar_color = 'green'
    elif percent < 80:
        bar_color = 'yellow'
    else:
        bar_color = 'red'
    bar = c('█' * filled_len, bar_color, bright=True) + c('░' * (bar_length - filled_len), 'white')
    prefix_col = c(prefix, 'cyan', bright=True)
    suffix_col = c(suffix, 'white')
    percent_str = c(f"{percent:.1f}%", 'yellow', bright=True) if show_percent else ''
    sys.stdout.write(f'\r{prefix_col} │{bar}│ {percent_str} {suffix_col}')
    sys.stdout.flush()
    if current == total:
        print()

# ------------------------------------------------------------
# Баннер программы
# ------------------------------------------------------------
def print_banner():
    """Печатает красивый ASCII-баннер OSINT AI."""
    banner_lines = [
        "  ╔══════════════════════════════════════════════════════════╗",
        "  ║   ██████╗ ███████╗██╗███╗   ██╗████████╗                 ║",
        "  ║  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝                 ║",
        "  ║  ██║   ██║███████╗██║██╔██╗ ██║   ██║                    ║",
        "  ║  ██║   ██║╚════██║██║██║╚██╗██║   ██║                    ║",
        "  ║  ╚██████╔╝███████║██║██║ ╚████║   ██║                    ║",
        "  ║   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝                    ║",
        "  ║                                                          ║",
        "  ║      OSINT AI HELPER v13.97 — Professional Edition       ║",
        "  ║      \"Ethical intelligence, responsible discovery\"       ║",
        "  ╚══════════════════════════════════════════════════════════╝",
    ]
    colors = ['red', 'yellow', 'green', 'cyan', 'magenta']
    for i, line in enumerate(banner_lines):
        col = colors[i % len(colors)]
        animated_print(line, delay=0.01, color=col, bright=True)
    print()

# ------------------------------------------------------------
# Умный вывод результата с распознаванием типов строк
# ------------------------------------------------------------
def print_result(text, title=None, animate=False, title_color='cyan'):
    """
    Выводит результат команды с автоматическим форматированием.
    Распознаёт строки, начинающиеся с [+], [-], [!], [i], и URL/IP.
    """
    if title:
        print_header(title, color=title_color)
    if animate:
        animated_print(text, delay=0.008)
    else:
        for line in text.split('\n'):
            if not line.strip():
                print()
                continue
            if line.startswith('[+]'):
                print_success(line[3:].strip())
            elif line.startswith('[-]'):
                print_error(line[3:].strip())
            elif line.startswith('[i]'):
                print_info(line[3:].strip())
            elif line.startswith('[!]'):
                print_warning(line[3:].strip())
            elif line.endswith(':') and not line.startswith(' '):
                print_section(line.rstrip(':'))
            else:
                if re.search(r'https?://', line):
                    print(c(line, 'blue', underline=True))
                elif re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line):
                    print(c(line, 'teal'))
                else:
                    print(line)
