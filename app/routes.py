from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.models import TaskCreate, TaskResponse, ErrorResponse
from app.storage import TaskStorage

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)

storage = TaskStorage()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой задачи",
    description="""
    ### Создает новую задачу в системе.
    
    **Процесс создания:**
    1. Принимает JSON с данными задачи
    2. Валидирует все поля
    3. Генерирует уникальный идентификатор (UUID v4)
    4. Добавляет временную метку создания (UTC)
    5. Сохраняет задачу в памяти
    6. Возвращает созданную задачу с идентификатором
    """,
    responses={
        201: {
            "description": "✅ Задача успешно создана",
            "model": TaskResponse,
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Разработать дизайн главной страницы",
                        "description": "Создать макет с учетом нового брендбука",
                        "priority": 3,
                        "created_at": "2026-06-21T10:30:00.000Z"
                    }
                }
            }
        },
        422: {
            "description": "❌ Ошибка валидации входных данных",
            "content": {
                "application/json": {
                    "examples": {
                        "short_title": {
                            "summary": "Название слишком короткое (менее 3 символов)",
                            "value": {
                                "detail": [
                                    {
                                        "type": "string_too_short",
                                        "loc": ["body", "title"],
                                        "msg": "String should have at least 3 characters",
                                        "input": "AB",
                                        "ctx": {"min_length": 3}
                                    }
                                ],
                                "status_code": 422
                            }
                        },
                        "invalid_priority": {
                            "summary": "Приоритет вне допустимого диапазона (должен быть 1-5)",
                            "value": {
                                "detail": [
                                    {
                                        "type": "greater_than_equal",
                                        "loc": ["body", "priority"],
                                        "msg": "Input should be greater than or equal to 1",
                                        "input": 0,
                                        "ctx": {"ge": 1}
                                    }
                                ],
                                "status_code": 422
                            }
                        },
                        "missing_title": {
                            "summary": "Отсутствует обязательное поле title",
                            "value": {
                                "detail": [
                                    {
                                        "type": "missing",
                                        "loc": ["body", "title"],
                                        "msg": "Field required",
                                        "input": {"priority": 3}
                                    }
                                ],
                                "status_code": 422
                            }
                        }
                    }
                }
            }
        }
    }
)
async def create_task(task: TaskCreate):
    """Создает новую задачу."""
    return storage.create_task(task)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получение задачи по идентификатору",
    description="""
    ### Возвращает полную информацию о задаче по её уникальному идентификатору.
    
    **Параметры запроса:**
    - task_id (path): Уникальный идентификатор задачи в формате UUID v4
    """,
    responses={
        200: {
            "description": "✅ Задача успешно найдена",
            "model": TaskResponse,
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Разработать дизайн главной страницы",
                        "description": "Создать макет с учетом нового брендбука",
                        "priority": 3,
                        "created_at": "2026-06-21T10:30:00.000Z"
                    }
                }
            }
        },
        404: {
            "description": "❌ Задача не найдена",
            "content": {
                "application/json": {
                    "examples": {
                        "task_not_found": {
                            "summary": "Задача с указанным ID отсутствует",
                            "value": {
                                "detail": "Задача с идентификатором '123e4567-e89b-12d3-a456-426614174001' не найдена. Проверьте корректность ID.",
                                "status_code": 404
                            }
                        },
                        "invalid_uuid_format": {
                            "summary": "Неверный формат UUID",
                            "value": {
                                "detail": "Задача с идентификатором 'invalid-uuid' не найдена. Проверьте корректность ID.",
                                "status_code": 404
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_task(task_id: str):
    """Получает задачу по её уникальному идентификатору."""
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с идентификатором '{task_id}' не найдена. Проверьте корректность ID."
        )
    return task


@router.get(
    "",
    summary="Получение списка всех задач",
    description="""
    ### Возвращает список всех существующих задач.
    
    **Полезно для:**
    - Отладки и тестирования
    - Получения полного списка задач
    - Проверки содержимого хранилища
    """,
    response_model=list[TaskResponse],
    responses={
        200: {
            "description": "✅ Список задач успешно получен",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Разработать дизайн главной страницы",
                            "description": "Создать макет с учетом нового брендбука",
                            "priority": 3,
                            "created_at": "2026-06-21T10:30:00.000Z"
                        }
                    ]
                }
            }
        }
        # ⚠️ НЕТ секций 404 и 422 - GET без параметров всегда возвращает 200
    }
)
async def get_all_tasks():
    """Получает все задачи из хранилища."""
    return storage.get_all_tasks()


@router.delete(
    "/{task_id}",
    summary="Удаление задачи по идентификатору",
    description="""
    ### Удаляет задачу из хранилища по её идентификатору.
    
    **Процесс удаления:**
    1. Поиск задачи в хранилище по ID
    2. Если задача найдена - удаление из хранилища
    3. Возврат сообщения об успешном удалении
    4. Если задача не найдена - ошибка 404
    """,
    responses={
        200: {
            "description": "✅ Задача успешно удалена",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Задача успешно удалена",
                        "task_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                }
            }
        },
        404: {
            "description": "❌ Задача не найдена",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Задача с идентификатором '123e4567-e89b-12d3-a456-426614174001' не найдена",
                        "status_code": 404
                    }
                }
            }
        }
    }
)
async def delete_task(task_id: str):
    """Удаляет задачу по идентификатору."""
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с идентификатором '{task_id}' не найдена"
        )
    return {
        "message": "Задача успешно удалена",
        "task_id": task_id
    }