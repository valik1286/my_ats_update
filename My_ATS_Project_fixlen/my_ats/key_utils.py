import datetime
import random
import string

# --- Генерація ключа ---
def create_key_ats():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    key = f"ATS{timestamp}{random_part}"
    return key

# --- Валідація ключа ---
def start_with_key(key: str):
    if not key.startswith("ATS"):
        raise ValueError("Ключ недійсний: не починається з 'ATS'.")
    if len(key) != 28: # Перевірка довжини
        raise ValueError("Ключ недійсний: неправильна довжина.")

    # Додаткові перевірки (можна додати перевірку дати, якщо вона закодована)
    # Наприклад:
    # try:
    #     timestamp_str = key[3:17] # 14 символів дати-часу
    #     key_datetime = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
    #     if key_datetime > datetime.datetime.now():
    #         raise ValueError("Ключ недійсний: дата в майбутньому.")
    # except ValueError:
    #     raise ValueError("Ключ недійсний: помилка в форматі дати.")

    print(f"АТС успішно запущено з ключем: {key}")