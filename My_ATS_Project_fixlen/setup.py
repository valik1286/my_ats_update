from setuptools import setup, find_packages

setup(
    name='my_ats',
    version='2.0.3', # Можливо, захочеш збільшити версію, наприклад, 2.1.0
    packages=find_packages(),
    include_package_data=True, # Важливо: включити дані з MANIFEST.in
    package_data={
        'my_ats': [ # 'my_ats' - це назва твого пакету
            'ai_knowledge.txt',
            'mods/*.py',  # Включаємо всі .py файли в папці mods
            'mods/*.ats', # Включаємо всі .ats файли в папці mods
            # Якщо є інші типи файлів у mods, додай їх сюди
        ],
    },
    # Додаємо entry_points, щоб можна було запускати АТС як команду (опціонально, але зручно)
    entry_points={
        'console_scripts': [
            'run-ats = my_ats.ats_runner:start_chat_console', # Будемо використовувати цю функцію
        ],
    },
    # ... інші метадані ...
)