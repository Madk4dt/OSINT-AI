# s3_bucket_check.py
# USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION
import requests
from utils import check_internet

def check_s3_bucket(bucket_name):
    if not check_internet():
        return "Нет интернета", []
    # Проверка только публичного листинга (без API)
    url = f"http://{bucket_name}.s3.amazonaws.com/"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            if '<ListBucketResult' in r.text or 'Contents' in r.text:
                return f"[!] Бакет {bucket_name} публично доступен для листинга!\nURL: {url}", []
            else:
                return f"Бакет {bucket_name} существует, но листинг запрещён (код 200, но не XML)", []
        elif r.status_code == 403:
            return f"Бакет {bucket_name} существует, но доступ запрещён (403)", []
        elif r.status_code == 404:
            return f"Бакет {bucket_name} не существует", []
        else:
            return f"Бакет {bucket_name}: код {r.status_code}", []
    except Exception as e:
        return f"Ошибка: {e}", []