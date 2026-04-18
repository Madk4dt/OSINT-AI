# phone.py (исходный)
import phonenumbers
from utils import t, check_internet, is_valid_phone
from config import SOURCES_DB

def phone_lookup(phone):
    if not check_internet(): return t("no_internet"), []
    if not is_valid_phone(phone): return t("invalid_phone"), []
    lines = [t("phone_title", phone), ""]
    try:
        parsed = phonenumbers.parse(phone, None)
        lines.append(t("phone_country", phonenumbers.region_code_for_number(parsed)))
        lines.append(t("phone_valid", "да"))
        lines.append(t("phone_operator", "требуется API (NumVerify)"))
    except Exception as e:
        lines.append(t("phone_error", str(e)))
    return "\n".join(lines), SOURCES_DB.get("phone", [])