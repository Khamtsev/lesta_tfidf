# Веб-приложение для рассчета TFIDF текстовых файлов
# Реализовано на Python 3.12.9 и Django 5.2

## Локальное развертывание

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Khamtsev/lesta_tfidf
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примините миграции
```bash
python manage.py migrate
```

5. Запустите приложение
```bash
python manage.py runserver
```

Приложение будет доступно по адресу:
<http://127.0.0.1:8000/>

Загрузите текстовый файл для подсчета TF, IDF, TFIDF. Для IDF и TFIDF учитываются все загруженные файлы.