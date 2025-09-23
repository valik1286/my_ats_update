import my_ats
import os

# Шлях до файлу, де зберігатиметься ключ
KEY_STORAGE_FILE = "ats_key_storage.txt"

def read_key_from_storage():
    """Читає ключ з файлу-сховища."""
    if os.path.exists(KEY_STORAGE_FILE):
        with open(KEY_STORAGE_FILE, 'r') as f:
            return f.read().strip()
    return None

def write_key_to_storage(key):
    """Зберігає ключ у файлі-сховищі."""
    with open(KEY_STORAGE_FILE, 'w') as f:
        f.write(key)
    print(f"Ключ успішно збережено у файлі '{KEY_STORAGE_FILE}'.")

def delete_key_from_storage():
    """Видаляє файл-сховище з ключем."""
    if os.path.exists(KEY_STORAGE_FILE):
        os.remove(KEY_STORAGE_FILE)
        print("Минулий ключ видалено.")
    else:
        print("Ключ не знайдено, видаляти нічого.")

def main_launcher():
    """Основна функція для управління ключем і запуску АТС."""
    stored_key = read_key_from_storage()

    if stored_key:
        print(f"Знайдено збережений ключ: {stored_key}")
        action = input("Хочеш використати його (т), змінити (з), чи видалити (в)? ").lower()
        
        if action in ['т', '1']:
            key_to_use = stored_key
        elif action in ['з']:
            key_to_use = input("Введи новий API ключ АТС: ")
            save_prompt = input("Зберегти новий ключ (т/н)? ").lower()
            if save_prompt in ['т', '1']:
                write_key_to_storage(key_to_use)
            elif save_prompt in ['н', '0']:
                print("Ключ не буде збережено.")
        elif action in ['в', '0']:
            delete_key_from_storage()
            key_to_use = input("Введи ключ для поточного сеансу: ")
            save_prompt = input("Зберегти ключ для майбутнього використання (т/н)? ").lower()
            if save_prompt in ['т', '1']:
                write_key_to_storage(key_to_use)
            elif save_prompt in ['н', '0']:
                print("Ключ не буде збережено.")
        else:
            print("Невідомий вибір. Використовую збережений ключ.")
            key_to_use = stored_key
    else:
        key_to_use = input("Введи API ключ АТС: ")
        save_prompt = input("Зберегти ключ для майбутнього використання (т/н)? ").lower()
        if save_prompt in ['т', '1']:
            write_key_to_storage(key_to_use)
        elif save_prompt in ['н', '0']:
            print("Ключ не буде збережено.")

    print("\n--- Запуск АТС ---")
    try:
        my_ats.start_with_key(key_to_use)
        my_ats.start_chat(key_to_use)
        print("-" * 40)
        print("Робота АТС завершена.")
    except ValueError as e:
        print(f"Помилка: Наданий АТС ключ '{key_to_use}' недійсний: {e}")
        print("Будь ласка, перевірте ключ і спробуйте знову.")
    except Exception as e:
        print(f"Виникла непередбачена помилка під час роботи АТС: {e}")

if __name__ == "__main__":
    main_launcher()