from fastapi import FastAPI
from app.routes import router
from datetime import datetime

# Создание приложения с метаданными
app = FastAPI(
    title="Task Manager API",
    description="""
    ## 📋 Управление задачами с помощью REST API
    
    Этот API предоставляет полнофункциональный интерфейс для управления задачами.
    Реализован на FastAPI с автоматической генерацией документации.
    
    ### 🚀 Основные возможности:
    
    - **Создание задачи** — добавление новой задачи с указанием приоритета
    - **Получение задачи** — просмотр деталей задачи по ID
    - **Список всех задач** — получение всех задач (для разработки)
    - **Удаление задачи** — удаление задачи по ID
    
    ### 📊 Модель задачи:
    
    | Поле | Тип | Описание |
    |------|-----|----------|
    | id | UUID | Уникальный идентификатор |
    | title | string | Название (3-100 символов) |
    | description | string | Описание (до 500 символов) |
    | priority | integer | Приоритет (1-5) |
    | created_at | datetime | Время создания (UTC) |
    
    ### ⚠️ Важно:
    
    - Данные хранятся **только в памяти** сервера
    - При перезапуске все задачи будут потеряны
    - Каждая задача получает уникальный UUID v4
    - Для production рекомендуется использовать базу данных
    
    ### 🔐 Безопасность:
    
    В текущей версии аутентификация не требуется.
    Для production рекомендуется добавить JWT-аутентификацию.
    """,
    version="1.0.0",
    contact={
        "name": "API Support Team",
        "email": "support@taskmanager.example.com",
        "url": "https://github.com/yourusername/task-manager-api"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Задачи",
            "description": "Эндпоинты для управления задачами. Включает создание, чтение, обновление и удаление."
        },
        {
            "name": "Система",
            "description": "Системные эндпоинты для проверки работоспособности и получения информации."
        }
    ]
)

# Подключение роутера с маршрутами задач
app.include_router(router)


@app.get(
    "/",
    tags=["Система"],
    summary="Корневой эндпоинт API",
    description="""
    ### Проверка работоспособности API
    
    Возвращает приветственное сообщение и ссылки на документацию.
    
    **Использование:**
    - Проверка, что сервер запущен
    - Получение информации о версии API
    - Быстрый доступ к документации
    
    **Ответ:**
    - message (str): Приветственное сообщение
    - version (str): Версия API
    - endpoints (dict): Ссылки на документацию
    """,
    responses={
        200: {
            "description": "✅ Успешный ответ",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Task Manager API",
                        "version": "1.0.0",
                        "endpoints": {
                            "docs": "/docs",
                            "redoc": "/redoc",
                            "openapi": "/openapi.json"
                        }
                    }
                }
            }
        }
    }
)
async def root():
    """
    Корневой эндпоинт для проверки работоспособности.
    
    Returns:
        dict: Информация об API и ссылки на документацию
    """
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


@app.get(
    "/health",
    tags=["Система"],
    summary="Проверка здоровья сервиса",
    description="""
    ### Эндпоинт для мониторинга состояния сервиса
    
    Используется для проверки, что приложение работает корректно.
    Полезен для систем мониторинга (Kubernetes, Prometheus, и т.д.).
    
    **Использование:**
    - Health checks в Kubernetes
    - Мониторинг доступности сервиса
    - Проверка перед деплоем
    
    **Ответ:**
    - status (str): "healthy" если все работает
    - timestamp (datetime): Время проверки в UTC
    """,
    responses={
        200: {
            "description": "✅ Сервис здоров",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2026-06-21T10:30:00.000Z",
                        "version": "1.0.0"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Проверка состояния сервиса для мониторинга.
    
    Returns:
        dict: Статус здоровья сервиса
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )