# Task Manager API

Простое REST API для управления задачами, реализованное на FastAPI.

## Особенности

- Создание задач с приоритетом
- Получение задач по ID
- Автоматическая документация Swagger UI
- Валидация данных через Pydantic
- Хранение в памяти (для демонстрации)

- / - Возвращает приветственное сообщение и ссылки на документацию.
- /health - Эндпоинт для мониторинга состояния сервиса

## Установка и Запуск сервера

1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   git clone https://github.com/mozgozjegatel/task_manager_api.git
   cd task_manager_api
   python3 -m venv venv 
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000