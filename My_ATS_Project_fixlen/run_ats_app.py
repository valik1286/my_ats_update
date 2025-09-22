# My_ATS_Project_fixlen.zip/run_ats_app.py
from my_ats import create_key_ats, start_with_key

def demo():
    print("Генерую новий АТС ключ...")
    key = create_key_ats()
    print("Тестую запуск АТС з згенерованим ключем...")
    try:
        start_with_key(key)
    except ValueError as e:
        print(f"Помилка під час запуску АТС: {e}")

if __name__ == "__main__":
    demo()