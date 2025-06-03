# Веб-приложение для расчета TFIDF текстовых файлов - v0.2.0

Веб-приложение для анализа текстовых файлов с использованием метрик TF (Term Frequency), IDF (Inverse Document Frequency) и TFIDF (Term Frequency-Inverse Document Frequency).

## Технологии

- Python 3.12.9
- Django 5.2
- PostgreSQL
- Docker & Docker Compose

## Локальное развертывание

### Требования

- Docker
- Docker Compose
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Khamtsev/lesta_tfidf
cd lesta_tfidf
```

2. Создайте и заполните файл .env на основе .env.example:
```bash
cp .env.example .env
```

3. Запустите проект с помощью Docker Compose:
```bash
docker compose up --build
```

Приложение будет доступно по адресу:
http://localhost

## Использование

1. Загрузите текстовый файл для подсчета TF, IDF, TFIDF
2. Для расчета IDF и TFIDF учитываются все загруженные файлы
3. Результаты анализа будут отображены в веб-интерфейсе

### API Endpoints

Приложение предоставляет следующие API эндпоинты:

- `GET /api/status/` - проверка статуса приложения
- `GET /api/version/` - получение текущей версии приложения
- `GET /api/metrics/` - получение метрик обработки файлов в формате JSON:
  - `files_processed` - количество обработанных файлов
  - `min_time_processed` - минимальное время обработки файла
  - `avg_time_processed` - среднее время обработки файла
  - `max_time_processed` - максимальное время обработки файла
  - `latest_file_processed_timestamp` - время последней обработки файла
  - `avg_file_size` - средний размер файла. Вместе с `avg_time_processed` может быть полезно для представления о времени обработки файлов.

## Структура проекта

```
lesta_tfidf/
├── core/           # API приложение
├── core/           # Основное приложение
├── tfidf/          # Конфигурация проекта Django
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Переменные окружения

Основные переменные окружения (определяются в .env):
- `DEBUG` - режим отладки Django (1 - включен, 0 - выключен)
- `SECRET_KEY` - секретный ключ Django для безопасности
- `ALLOWED_HOSTS` - список разрешенных хостов для Django
- `POSTGRES_DB` - имя базы данных PostgreSQL
- `POSTGRES_USER` - пользователь базы данных PostgreSQL
- `POSTGRES_PASSWORD` - пароль базы данных PostgreSQL
- `DB_HOST` - хост базы данных (в Docker Compose это имя сервиса)
- `DB_PORT` - порт базы данных PostgreSQL (по умолчанию 5432)
