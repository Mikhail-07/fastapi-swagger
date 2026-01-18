# Отчет: Развертывание и работа WebGL/WebGPU Glossary API

## Описание проекта

REST API для управления глоссарием терминов WebGL/WebGPU, реализованный с использованием FastAPI, SQLite и Pydantic для валидации данных. API предоставляет полный набор CRUD операций и автоматическую интерактивную документацию через Swagger UI.

## Технологический стек

- **FastAPI** - современный веб-фреймворк для создания API на Python
- **SQLite** - встроенная база данных для хранения терминов
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация и сериализация данных
- **Uvicorn** - ASGI сервер для запуска приложения
- **Swagger/OpenAPI** - автоматическая генерация документации API

## Структура проекта

```
fastapi-swagger/
├── main.py           # Основное приложение FastAPI с эндпоинтами
├── database.py       # Конфигурация SQLAlchemy и подключение к БД
├── models.py         # SQLAlchemy модели (Term)
├── schemas.py        # Pydantic схемы для валидации
├── init_db.py        # Скрипт инициализации БД с примерами
├── requirements.txt  # Зависимости проекта
├── REPORT.md         # Данный отчет
└── glossary.db       # SQLite база данных (создается автоматически)
```

## Установка и развертывание

### Шаг 1: Установка зависимостей

Убедитесь, что у вас установлен Python 3.8 или выше, затем установите зависимости:

```bash
pip install -r requirements.txt
```

Или установите зависимости вручную:

```bash
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==2.0.23 pydantic==2.5.0
```

### Шаг 2: Инициализация базы данных

Запустите скрипт инициализации для создания таблиц и заполнения примерами терминов:

```bash
python init_db.py
```

Скрипт создаст:
- Таблицу `terms` в базе данных `glossary.db`
- 15 примеров терминов WebGL/WebGPU

### Шаг 3: Запуск сервера

Запустите FastAPI приложение:

```bash
python main.py
```

Или с использованием uvicorn напрямую:

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: `http://localhost:8000`

### Шаг 4: Доступ к документации API

После запуска сервера доступны следующие URL:

- **Swagger UI (интерактивная документация)**: `http://localhost:8000/docs`
- **ReDoc (альтернативная документация)**: `http://localhost:8000/redoc`
- **OpenAPI схема (JSON)**: `http://localhost:8000/openapi.json`

## API Эндпоинты

### 1. GET / - Корневой эндпоинт

Получение информации о API.

**Пример запроса:**
```bash
curl http://localhost:8000/
```

**Пример ответа:**
```json
{
  "message": "WebGL/WebGPU Glossary API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

### 2. GET /terms - Получение списка всех терминов

Возвращает список всех терминов в глоссарии.

**Пример запроса:**
```bash
curl http://localhost:8000/terms
```

**Пример ответа:**
```json
[
  {
    "id": 1,
    "keyword": "WebGL",
    "description": "Web Graphics Library - JavaScript API для рендеринга 2D и 3D графики в браузере без использования плагинов.",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": null
  },
  {
    "id": 2,
    "keyword": "WebGPU",
    "description": "Современный низкоуровневый API для графики и вычислений в веб-браузерах, преемник WebGL.",
    "created_at": "2024-01-01T12:00:01",
    "updated_at": null
  }
]
```

### 3. GET /terms/{keyword} - Получение термина по ключевому слову

Возвращает информацию о конкретном термине по его ключевому слову.

**Пример запроса:**
```bash
curl http://localhost:8000/terms/WebGL
```

**Пример ответа:**
```json
{
  "id": 1,
  "keyword": "WebGL",
  "description": "Web Graphics Library - JavaScript API для рендеринга 2D и 3D графики в браузере без использования плагинов.",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": null
}
```

**Ошибка (термин не найден):**
```json
{
  "detail": "Термин с ключевым словом 'NonExistent' не найден"
}
```

### 4. POST /terms - Создание нового термина

Добавляет новый термин в глоссарий.

**Пример запроса:**
```bash
curl -X POST "http://localhost:8000/terms" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "Render Pass",
    "description": "Этап рендеринга, определяющий операции, выполняемые над набором прикреплений."
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 16,
  "keyword": "Render Pass",
  "description": "Этап рендеринга, определяющий операции, выполняемые над набором прикреплений.",
  "created_at": "2024-01-01T12:30:00",
  "updated_at": null
}
```

**Ошибка (термин уже существует):**
```json
{
  "detail": "Термин с ключевым словом 'WebGL' уже существует"
}
```

### 5. PUT /terms/{keyword} - Обновление существующего термина

Обновляет информацию о существующем термине.

**Пример запроса:**
```bash
curl -X PUT "http://localhost:8000/terms/WebGL" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Обновленное описание WebGL с дополнительной информацией."
  }'
```

**Пример ответа:**
```json
{
  "id": 1,
  "keyword": "WebGL",
  "description": "Обновленное описание WebGL с дополнительной информацией.",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T13:00:00"
}
```

**Можно обновить оба поля:**
```bash
curl -X PUT "http://localhost:8000/terms/WebGL" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "WebGL2",
    "description": "Вторая версия WebGL с расширенными возможностями."
  }'
```

**Ошибка (термин не найден):**
```json
{
  "detail": "Термин с ключевым словом 'NonExistent' не найден"
}
```

### 6. DELETE /terms/{keyword} - Удаление термина

Удаляет термин из глоссария.

**Пример запроса:**
```bash
curl -X DELETE "http://localhost:8000/terms/WebGL"
```

**Ответ:** 204 No Content (тело ответа отсутствует)

**Ошибка (термин не найден):**
```json
{
  "detail": "Термин с ключевым словом 'NonExistent' не найден"
}
```

## Использование Swagger UI

Swagger UI предоставляет интерактивный интерфейс для тестирования всех эндпоинтов API:

1. Откройте `http://localhost:8000/docs` в браузере
2. Выберите интересующий эндпоинт из списка
3. Нажмите "Try it out" для активации формы
4. Заполните необходимые параметры (для POST/PUT укажите JSON в теле запроса)
5. Нажмите "Execute" для выполнения запроса
6. Просмотрите ответ сервера в разделе "Responses"

### Примеры использования Swagger UI

#### Создание термина через Swagger:
1. Разверните секцию `POST /terms`
2. Нажмите "Try it out"
3. Замените пример JSON на:
```json
{
  "keyword": "Pipeline State",
  "description": "Состояние графического конвейера, включающее шейдеры и настройки рендеринга."
}
```
4. Нажмите "Execute"

#### Получение термина:
1. Разверните секцию `GET /terms/{keyword}`
2. Нажмите "Try it out"
3. В поле `keyword` введите: `WebGPU`
4. Нажмите "Execute"

## Валидация данных

API использует Pydantic для валидации входных данных:

- **TermCreate**: оба поля (`keyword`, `description`) обязательны
  - `keyword`: от 1 до 100 символов
  - `description`: минимум 1 символ

- **TermUpdate**: оба поля опциональны, но должны соответствовать тем же правилам при указании

**Пример ошибки валидации:**
```json
{
  "detail": [
    {
      "loc": ["body", "keyword"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

## Структура базы данных

Таблица `terms`:

| Поле        | Тип       | Описание                    |
|-------------|-----------|-----------------------------|
| id          | INTEGER   | Первичный ключ              |
| keyword     | TEXT      | Ключевое слово (уникальное) |
| description | TEXT      | Описание термина            |
| created_at  | DATETIME  | Дата создания               |
| updated_at  | DATETIME  | Дата обновления (nullable)  |

## Особенности реализации

1. **Dependency Injection**: Использование FastAPI dependency injection для управления сессиями БД
2. **Автоматическая документация**: Swagger/OpenAPI схема генерируется автоматически
3. **Валидация**: Все входные данные валидируются через Pydantic
4. **Обработка ошибок**: Корректная обработка 404 и 400 ошибок
5. **Уникальность**: Гарантия уникальности ключевых слов на уровне БД и API
6. **Timestamps**: Автоматическое отслеживание времени создания и обновления

## Тестирование API

### Использование cURL

Все примеры запросов доступны выше в разделе "API Эндпоинты".

### Использование Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Получение всех терминов
response = requests.get(f"{BASE_URL}/terms")
print(response.json())

# Получение конкретного термина
response = requests.get(f"{BASE_URL}/terms/WebGL")
print(response.json())

# Создание термина
new_term = {
    "keyword": "Pipeline",
    "description": "Графический конвейер обработки данных."
}
response = requests.post(f"{BASE_URL}/terms", json=new_term)
print(response.json())

# Обновление термина
update_data = {
    "description": "Обновленное описание Pipeline."
}
response = requests.put(f"{BASE_URL}/terms/Pipeline", json=update_data)
print(response.json())

# Удаление термина
response = requests.delete(f"{BASE_URL}/terms/Pipeline")
print(response.status_code)  # 204
```

## Возможные улучшения

1. Добавление пагинации для списка терминов
2. Реализация поиска по описанию
3. Добавление категорий/тегов для терминов
4. Реализация аутентификации и авторизации
5. Добавление версионирования API
6. Логирование запросов и ошибок
7. Добавление rate limiting
8. Миграции базы данных через Alembic

## Заключение

API успешно реализован и готов к использованию. Все CRUD операции работают корректно, валидация данных обеспечивает целостность информации, а автоматическая документация Swagger упрощает тестирование и интеграцию.

