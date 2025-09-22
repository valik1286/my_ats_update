import datetime
import os
import sys
import re
import importlib.resources as pkg_resources # Новий імпорт для доступу до ресурсів пакета

# --- ІМПОРТУЄМО НАШІ ВЛАСНІ ФУНКЦІЇ З ЦЬОГО Ж ПАКЕТУ ---
from .key_utils import start_with_key # Змінено: імпортуємо з key_utils.py

# --- Конфігурація ---
AI_NAME = "AT-S"
VERSION = "1.6.2"
AUTHOR = "valik1286"
KNOWLEDGE_BASE_FILENAME = "ai_knowledge.txt" # Змінено: тепер це ім'я файлу, а не шлях
MODS_FOLDER_NAME = "mods" # Змінено: тепер це ім'я папки, а не шлях

# --- Глобальні змінні ---
knowledge_base = {}

# --- Константи для аналізу ---
RED = "\033[91m"
RESET = "\033[0m"

# --- Функція для отримання шляху до ресурсів всередині пакета ---
def get_package_resource_path(filename):
    # 'my_ats' - це назва твого пакету
    return pkg_resources.files('my_ats').joinpath(filename)

# --- Функція для отримання шляху до папки модів всередині пакета ---
def get_mods_folder_path():
    return pkg_resources.files('my_ats').joinpath(MODS_FOLDER_NAME)

# --- Завантаження бази знань ---
def load_knowledge_base():
    knowledge = {}
    try:
        # Відкриваємо файл ai_knowledge.txt як ресурс пакету
        with pkg_resources.as_file(get_package_resource_path(KNOWLEDGE_BASE_FILENAME)) as knowledge_path:
            with open(knowledge_path, "r", encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        key, value = line.strip().split(":", 1)
                        knowledge[key.lower()] = value.strip()
    except FileNotFoundError:
        print(f"Попередження: Файл бази знань '{KNOWLEDGE_BASE_FILENAME}' не знайдено всередині пакету.")
    return knowledge

# --- Збереження бази знань ---
def save_knowledge_base(knowledge):
    # Збереження змінених знань потребує доступу до файлу, який може бути упакований.
    # Найкращий підхід - зберегти його у доступне для запису місце, наприклад, у папку користувача,
    # або ж змінити оригінальний файл, якщо він не є частиною zip-архіву пакету.
    # Для простоти, поки що, збережемо у поточну директорію запуску.
    # ЦЕ ВАЖЛИВИЙ МОМЕНТ: Збереження в "ресурс пакету" не завжди можливо після інсталяції.
    # Альтернатива: зберегти в AppData (Windows) або ~/.config (Linux)
    try:
        # Спроба зберегти в оригінальний файл, якщо пакет не встановлений як wheel/zip
        with pkg_resources.as_file(get_package_resource_path(KNOWLEDGE_BASE_FILENAME)) as knowledge_path:
             with open(knowledge_path, "w", encoding="utf-8") as f:
                for key, value in knowledge.items():
                    f.write(f"{key}: {value}\n")
    except Exception as e:
        print(f"Попередження: Не вдалося зберегти базу знань у пакет. Зберігаємо у поточну директорію. Помилка: {e}")
        # Якщо не вдалося зберегти в пакеті, зберігаємо у поточній робочій директорії
        with open(KNOWLEDGE_BASE_FILENAME, "w", encoding="utf-8") as f:
            for key, value in knowledge.items():
                f.write(f"{key}: {value}\n")


# --- Обробка відповіді (без змін) ---
def get_response(user_input, knowledge_base):
    user_input_lower = user_input.lower().strip()

    if user_input_lower.startswith("навчи "):
        parts = user_input[len("навчи "):].strip().split(" це ", 1)
        if len(parts) == 2:
            phrase = parts[0].strip()
            meaning = parts[1].strip()
            knowledge_base[phrase.lower()] = meaning
            save_knowledge_base(knowledge_base)
            return f"Запам'ятано: '{phrase}' означає '{meaning}'."
        else:
            return "Невірний формат. Використовуйте: навчи слово це значення."

    if user_input_lower == "вийти":
        print("До побачення, Користувач! Був радий поспілкуватися.")
        sys.exit(0)  # <-- тут додаємо реальне завершення
    elif user_input_lower == "про мене":
        return f"{AI_NAME} - версія {VERSION} від {AUTHOR}. Я твій персональний помічник, що чекає на команди."
    elif user_input_lower == "допомога":
        help_text = (
            "Доступні команди:\n"
            "вийти - завершити розмову\n"
            "про мене - інформація про АТС\n"
            "допомога - цей список команд\n"
            "навчи слово це значення - додати нове слово до знань АТС\n"
            "Зверни увагу: АТС зараз працює в обмеженому режимі."
        )
        return help_text

    for key, value in knowledge_base.items():
        if key in user_input_lower:
            return value

    return "Я не розумію. Спробуй 'допомога'."


# --- Завантаження динамічних модів з папки 'mods' ---
def load_mods():
    # Шлях до папки mods тепер отримується як ресурс пакету
    mods_path_obj = get_mods_folder_path()
    
    # sys.path.insert(0, str(mods_path_obj)) # Додаємо шлях до модів для імпорту

    loaded_mods = []
    
    # Використовуємо try-except для обробки випадку, якщо папка mods не існує
    try:
        with pkg_resources.as_file(mods_path_obj) as mods_path_fs:
            # Тепер ми можемо працювати з mods_path_fs як зі звичайним шляхом на файловій системі
            if not os.path.exists(mods_path_fs):
                os.makedirs(mods_path_fs) # Створюємо, якщо не існує
            
            # Додаємо шлях до sys.path тільки тут, щоб __import__ працював
            sys.path.insert(0, str(mods_path_fs))

            for filename in os.listdir(mods_path_fs):
                if filename.endswith(".py") or filename.endswith(".ats"):
                    module_name = filename[:-3]
                    try:
                        mod = __import__(module_name)
                        loaded_mods.append(mod)
                        print(f"Завантажено мод: {module_name}")
                    except Exception as e:
                        print(f"Помилка завантаження мода {filename}: {e}")
    except FileNotFoundError:
        print(f"Попередження: Папка модів '{MODS_FOLDER_NAME}' не знайдена всередині пакету.")
    except Exception as e:
        print(f"Помилка доступу до папки модів всередині пакету: {e}")
        print("Можливо, пакет встановлений як zip-архів, і доступ до файлів у ньому обмежений.")

    return loaded_mods
    
# --- Основний цикл ---
def start_chat(ats_key: str):
    print(f"Привіт! Я {AI_NAME}. Ти запустив мене з ключем. Перевіряю...")
    
    try:
        start_with_key(ats_key)
    except ValueError as e:
        print(f"{RED}Помилка запуску АТС: {e}{RESET}")
        print("Завершення роботи. Ключ недійсний або не наш.")
        sys.exit(1)

    global knowledge_base
    knowledge_base = load_knowledge_base()
    
    loaded_mods = load_mods()

    print(f"АТС {AI_NAME} (версія {VERSION}) успішно запущена. Готовий до роботи, Користувач!")
    print("Пиши 'допомога' для списку команд.")

    while True:
        user_input = input("Ти: ").strip()
        
        mod_handled = False
        for mod in loaded_mods:
            if hasattr(mod, 'handle_command'):
                mod_response = mod.handle_command(user_input)
                if mod_response:
                    print(f"{AI_NAME} (мод {mod.__name__}): {mod_response}")
                    mod_handled = True
                    break
        
        if not mod_handled:
            response = get_response(user_input, knowledge_base)
            print(f"{AI_NAME}: {response}")

# --- Обгортка для запуску з консолі (якщо ти використовуєш entry_points) ---
def start_chat_console():
    if len(sys.argv) < 2:
        print(f"{RED}Використання: run-ats [АТС_КЛЮЧ]{RESET}")
        print("приклад: run-ats my_secret_key")
        sys.exit(1)
    
    ats_key = sys.argv[1]
    start_chat(ats_key)
