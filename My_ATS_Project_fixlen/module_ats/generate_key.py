import subprocess
import os

file_path = "C:\\Users\\Admin\\Desktop\\My_ATS_Project_fixlen\\run_ats_app.py"

if not os.path.exists(file_path):
    print(f"Помилка: файл не знайдено за шляхом {file_path}")
else:
    print("Запускаю файл run_ats_app.py...")
    try:
        # Змінюємо кодування на 'cp1251'
        result = subprocess.run(['python', file_path], capture_output=True, text=True, check=True, encoding='cp1251')
        
        print("\n--- Результат виконання ---\n")
        print(result.stdout)
        
        if result.stderr:
            print("\n--- Помилки ---\n")
            print(result.stderr)

    except FileNotFoundError:
        print("Помилка: Не знайдено 'python' в PATH. Переконайся, що Python встановлений і доданий до системних змінних PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка під час виконання файлу: {e}")
        print(f"Вивід помилки:\n{e.stderr}")
    except Exception as e:
        print(f"Виникла неочікувана помилка: {e}")

input("\nНатисни Enter, щоб вийти...")