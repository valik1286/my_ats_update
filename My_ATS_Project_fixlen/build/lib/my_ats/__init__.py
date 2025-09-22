# C:\Users\Admin\Desktop\My_ATS_Project_fixlen\my_ats\__init__.py

"""
my_ats package — ATS key generator & validator (no storage), guaranteed length 28.
"""

import random
import string
import hashlib
import re

# ДОДАЙ ЦЕЙ РЯДОК:
from .ats_runner import start_chat # <--- ЦЕЙ РЯДОК ДОДАЄТЬСЯ!

__all__ = ["create_key_ats", "start_with_key", "start_chat"] # <--- "start_chat" ДОДАЄТЬСЯ СЮДИ!

# Змінено шаблон для включення малих літер та подовжено останню частину для 28 символів
BASE_PATTERN = r"^ATS[a-zA-Z0-9]{4}S[a-zA-Z0-9]{5}E[a-zA-Z0-9]{4}D[a-zA-Z0-9]{7}$" # Змінено 5 на 7 для part4

def _rnd(n):
    # Додано малі літери до дозволених символів
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

def _checksum(base_key: str) -> str:
    h = hashlib.sha1(base_key.encode("utf-8")).hexdigest().upper()
    return h[:2]

def create_key_ats() -> str:
    """
    Generate ATS key in format ATS####S#####E####D#######CC
    (total length = 28). Regenerates if length mismatch.
    """
    while True:
        part1 = _rnd(4)
        part2 = _rnd(5)
        part3 = _rnd(4)
        part4 = _rnd(7) # Змінено 5 на 7, щоб додати 2 символи
        base_key = f"ATS{part1}S{part2}E{part3}D{part4}"
        chk = _checksum(base_key)
        full_key = base_key + chk
        print(f"Спроба генерації: {full_key} (довжина: {len(full_key)})") # Залишаємо для дебагу, якщо треба
        if len(full_key) == 28:
            print(f"Згенеровано новий АТС ключ: {full_key}")
            return full_key

def start_with_key(ats_key: str) -> bool:
    """
    Validate and 'start' ATS with given key.
    Returns True if valid, raises ValueError otherwise.
    """
    if not isinstance(ats_key, str):
        raise ValueError("АТС ключ має бути рядком")
    if len(ats_key) != 28:
        raise ValueError("Невірна довжина АТС ключа")
    base_part = ats_key[:-2]
    chk_part = ats_key[-2:]
    # Використання оновленого BASE_PATTERN
    if not re.match(BASE_PATTERN, base_part):
        raise ValueError("Невірний формат АТС ключа")
    if _checksum(base_part) != chk_part:
        raise ValueError("Невідповідність контрольної суми АТС ключа")
    print(f"АТС успішно запущено з ключем: {ats_key}")
    return True