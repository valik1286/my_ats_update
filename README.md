My_ATS Project
Опис

My_ATS — це персональний асистент (ATS), який працює з ключами доступу.
Він може:

відповідати на прості питання через базу знань (ai_knowledge.txt),

навчатися новим словам через команду навчи слово це значення,

запускати модулі (mods) для додаткової функціональності.

Проєкт побудований як пакет Python і може запускатися через консольну команду run-ats.

Встановлення

Клонуй репозиторій або завантаж ZIP:

git clone https://github.com/valik1286/my_ats_update.git
cd my_ats_update


Встанови пакет через pip:

pip install .


Це встановить пакет my_ats і додасть консольну команду run-ats.

Використання
Генерація ключа та запуск ATS з Python
from my_ats import create_key_ats, start_chat

# Генеруємо ключ
key = create_key_ats()

# Запускаємо ATS
start_chat(key)

Або через консоль:
run-ats <твій_ключ>

Команди всередині ATS

вийти — завершити сеанс.

про мене — інформація про ATS.

допомога — список доступних команд.

навчи слово це значення — додати нове слово до бази знань.

Додаткові скрипти
1️⃣ Генерація ключа (generate_key.py)
import subprocess
import os

file_path = os.path.join(os.path.dirname(__file__), "run_ats_app.py")

if not os.path.exists(file_path):
    print(f"Помилка: файл не знайдено за шляхом {file_path}")
else:
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True, check=True)
        print("\n--- Результат виконання ---\n")
        print(result.stdout)
        if result.stderr:
            print("\n--- Помилки ---\n")
            print(result.stderr)
    except Exception as e:
        print(f"Помилка під час виконання: {e}")

input("\nНатисни Enter, щоб вийти...")

2️⃣ Запуск ATS з фіксованим ключем (launch_ats.py)
import my_ats

ats_key = "ТУТ_ТВОЙ_КЛЮЧ"

def main_launcher():
    print("Запуск АТС з 'встановленим' ключем...")
    try:
        my_ats.start_with_key(ats_key)
        my_ats.start_chat(ats_key)
        print("Робота АТС завершена.")
    except ValueError as e:
        print(f"Помилка: ключ недійсний: {e}")
    except Exception as e:
        print(f"Непередбачена помилка: {e}")

if __name__ == "__main__":
    main_launcher()

3️⃣ Перевірка та управління ключем (check_key.py)
import my_ats
import os

KEY_STORAGE_FILE = "ats_key_storage.txt"

def read_key():
    if os.path.exists(KEY_STORAGE_FILE):
        with open(KEY_STORAGE_FILE, 'r') as f:
            return f.read().strip()
    return None

def write_key(key):
    with open(KEY_STORAGE_FILE, 'w') as f:
        f.write(key)
    print(f"Ключ збережено у '{KEY_STORAGE_FILE}'.")

def delete_key():
    if os.path.exists(KEY_STORAGE_FILE):
        os.remove(KEY_STORAGE_FILE)
        print("Ключ видалено.")

def main_launcher():
    stored_key = read_key()
    if stored_key:
        print(f"Знайдено ключ: {stored_key}")
        action = input("Використати (т), змінити (з), видалити (в)? ").lower()
        if action == 'т':
            key_to_use = stored_key
        elif action == 'з':
            key_to_use = input("Введи новий ключ: ")
            if input("Зберегти? (т/н) ").lower() == 'т':
                write_key(key_to_use)
        elif action == 'в':
            delete_key()
            key_to_use = input("Введи ключ для сеансу: ")
            if input("Зберегти? (т/н) ").lower() == 'т':
                write_key(key_to_use)
        else:
            print("Невідомий вибір, використовую збережений ключ.")
            key_to_use = stored_key
    else:
        key_to_use = input("Введи ключ: ")
        if input("Зберегти для майбутнього використання? (т/н) ").lower() == 'т':
            write_key(key_to_use)

    try:
        my_ats.start_with_key(key_to_use)
        my_ats.start_chat(key_to_use)
        print("Робота АТС завершена.")
    except ValueError as e:
        print(f"Помилка: ключ недійсний: {e}")
    except Exception as e:
        print(f"Непередбачена помилка: {e}")

if __name__ == "__main__":
    main_launcher()

Модифікації та модулі

Папка mods дозволяє додавати власні модулі Python або ATS-файли (.ats) для розширення функцій.
Модулі автоматично завантажуються при старті ATS.

Модуль повинен мати функцію:

def handle_command(user_input: str) -> str:
    # повертає рядок з відповіддю, або None

Ліцензії

Код: MIT (LICENSE_MIT.txt) — дозволяє використовувати, змінювати та поширювати код без обмежень, включно з комерційним використанням.

Контент (база знань, моди): Creative Commons Attribution-NonCommercial 4.0 (LICENSE_CC.txt) — дозволяє копіювати та змінювати контент тільки для некомерційного використання з обов’язковим вказанням авторства.

Синхронізація та оновлення

Якщо змінюєш ai_knowledge.txt або додаєш модулі в mods, ATS автоматично підхоплює зміни при наступному запуску.

Для оновлення пакету після зміни коду:

pip install --upgrade .


Для синхронізації з репозиторієм:

git pull origin main

Додаткові поради

Зберігай свій ATS ключ у безпечному місці.

Роби бекап бази знань перед значними змінами.

Не змінюй внутрішні файли пакету, якщо не впевнений у наслідках — краще додати новий модуль у mods.
