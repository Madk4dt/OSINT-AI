# legal.py
# Возвращает правовую информацию на текущем языке (из config.CURRENT_LANG)

def legal_disclaimer():
    from config import CURRENT_LANG
    if CURRENT_LANG == "ru":
        text = """
    ПРАВОВАЯ ИНФОРМАЦИЯ

    Данный инструмент предназначен ТОЛЬКО для авторизованного тестирования
    безопасности, OSINT-исследований и образовательных целей.

    Вы должны иметь явное письменное разрешение на сканирование или сбор
    информации о любой цели, которой вы не владеете.

    Несанкционированный доступ к компьютерным системам является незаконным
    в соответствии с:
    - Computer Fraud and Abuse Act (CFAA, США)
    - Computer Misuse Act (Великобритания)
    - аналогичными законами других стран

    Автор не несёт ответственности за неправомерное использование данного ПО.

    Используя этот инструмент, вы соглашаетесь, что будете применять его только
    к системам, которыми владеете, или на тестирование которых получили
    явное разрешение.
    """
    else:
        text = """
    LEGAL NOTICE

    This tool is designed for authorized security testing, OSINT research,
    and educational purposes only.

    You must have explicit written permission to scan or gather information
    about any target that you do not own.

    Unauthorized access to computer systems is illegal under:
    - Computer Fraud and Abuse Act (CFAA, USA)
    - Computer Misuse Act (UK)
    - similar legislation worldwide

    The author assumes no liability for misuse of this software.

    By using this tool, you agree that you will only use it on systems
    you own or have explicit permission to test.
    """
    return text, []