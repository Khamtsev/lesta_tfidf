# Веб-приложение для расчета TFIDF текстовых файлов - v0.1.1

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

## Структура проекта

```
lesta_tfidf/
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
