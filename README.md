# Веб-приложение для расчета TFIDF текстовых файлов - v0.3.0

Веб-приложение для анализа текстовых файлов с использованием метрик TF (Term Frequency) и IDF (Inverse Document Frequency).

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

## Использование

### Регистрация 

1. Создайте нового пользователя:
```
POST http://localhost/api/v1/auth/users/`
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password",
}
```

2. Получите JWT токен:
```
POST `POST /api/v1/auth/jwt/create/`
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Ответ будет содержать access и refresh токены:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

3. Используйте токен для запросов:
```
GET http://localhost/api/v1/documents/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Пример использования

1. Создание коллекции:
```
POST http://localhost/api/v1/collections/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
    "name": "My Collection",
    "description": "Collection for testing"
}
```

2. Загрузка документа:
```
POST http://localhost/api/v1/documents/
Authorization: Bearer <your_access_token>
Content-Type: multipart/form-data

file: <your_text_file.txt>
```

3. Добавление документа в коллекцию:
```
POST http://localhost/api/v1/collections/1/1/
Authorization: Bearer <your_access_token>
```

4. Получение статистики по документу:
```
GET http://localhost/api/v1/documents/1/statistics/
Authorization: Bearer <your_access_token>
```

Пример ответа:
```json
[
    {
        "collection_id": 1,
        "collection_name": "My Collection",
        "statistics": [
            {
                "word": "example",
                "tf": 0.05,
                "idf": 2.3
            },
            {
                "word": "test",
                "tf": 0.03,
                "idf": 1.8
            }
            // ... еще 48 слов
        ]
    }
]
```

### Документация

- `/api/v1/swagger/` - Swagger документация
- `/api/v1/redoc/` - Redoc документация

### API Endpoints

Приложение предоставляет следующие API эндпоинты:


#### Пользователи

- `POST /api/v1/auth/users/` - регистрация нового пользователя
- `GET /api/v1/auth/users/me/` - получение информации о текущем пользователе
- `PATCH /api/v1/auth/users/me/` - частичное обновление данных пользователя
- `PUT /api/v1/auth/users/me/` - полное обновление данных пользователя
- `DELETE /api/v1/auth/users/me/` - удаление текущего пользователя
- `POST /api/v1/auth/users/set_password/` - изменение пароля
- `POST /api/v1/auth/jwt/create/` - получение JWT токена
- `POST /api/v1/auth/jwt/refresh/` - обновление JWT токена
- `POST /api/v1/auth/jwt/verify/` - проверка JWT токена

#### Документы [требуется аутентификация, доступ только к своим документам]
- `GET /api/v1/documents/` - получение списка документов (id и название)
- `GET /api/v1/documents/<document_id>/` - получение содержимого документа
- `POST /api/v1/documents/` - загрузка нового документа
- `DELETE /api/v1/documents/<document_id>/` - удаление документа
- `GET /api/v1/documents/<document_id>/statistics/` - получение статистики по документу (50 наиболее редких слов с их TF и IDF)
- `GET /api/v1/documents/<document_id>/huffman/` - получение содержимого документа, закодированного Кодом Хаффмана

#### Коллекции [требуется аутентификация, доступ только к своим коллекциям]
- `GET /api/v1/collections/` - получение списка коллекций с id и списком документов
- `GET /api/v1/collections/<collection_id>/` - получение списка id документов в коллекции
- `POST /api/v1/collections/` - создание новой коллекции
- `DELETE /api/v1/collections/<collection_id>/` - удаление коллекции
- `POST /api/v1/collections/<collection_id>/<document_id>/` - добавление документа в коллекцию
- `DELETE /api/v1/collections/<collection_id>/<document_id>/` - удаление документа из коллекции
- `GET /api/v1/collections/<collection_id>/statistics/` - получение статистики по коллекции (50 наиболее редких слов с их TF и IDF)

#### Системные [публичный доступ]
- `GET /api/v1/status/` - проверка статуса приложения
- `GET /api/v1/version/` - получение текущей версии приложения
- `GET /api/v1/metrics/` - получение метрик обработки файлов в формате JSON:
  - `document_metrics` - метрики обработки документов:
    - `statistics_requests` - количество запросов статистики
    - `latest_statistics_processed_timestamp` - время последней обработки
    - `min_time_processed` - минимальное время обработки
    - `avg_time_processed` - среднее время обработки
    - `max_time_processed` - максимальное время обработки
    - `total_documents` - общее количество документов
  - `collection_metrics` - метрики обработки коллекций:
    - `statistics_requests` - количество запросов статистики
    - `latest_statistics_processed_timestamp` - время последней обработки
    - `min_time_processed` - минимальное время обработки
    - `avg_time_processed` - среднее время обработки
    - `max_time_processed` - максимальное время обработки
    - `avg_documents_per_collection` - среднее количество документов в коллекции

## Структура проекта

```
lesta_tfidf/
├── api/                  # API приложение
├── core/                 # Основное приложение
├── users/                # Приложение для работы с пользователями
├── tfidf/                # Конфигурация проекта Django
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Инструкции для сборки Docker образа
├── requirements.txt      # Зависимости Python
├── .env.example          # Пример файла с переменными окружения
├── README.md             # Документация проекта
└── CHANGELOG.md          # История изменений проекта
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
- `DB_PORT` - порт базы данных PostgreSQL
- `NGINX_PORT` - порт доступа к API
- `THROTTLE_ANON_RATE` - ограничение на количество запросов неавторизованных пользователей, по умолчанию 10/в минуту
- `THROTTLE_USER_RATE` - ограничение на количество запросов авторизованным пользователей, по умолчанию 100/в минуту
