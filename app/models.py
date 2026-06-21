from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid


class TaskCreate(BaseModel):
    """
    Модель для создания новой задачи.
    
    Используется при отправке POST-запроса на эндпоинт /tasks.
    Все поля проходят валидацию перед сохранением в хранилище.
    
    Attributes:
        title (str): Название задачи. Обязательное поле.
        description (Optional[str]): Подробное описание задачи. Необязательное поле.
        priority (int): Приоритет задачи. Обязательное поле, от 1 (низший) до 5 (высший).
    
    Example:
        {
            "title": "Разработать дизайн главной страницы",
            "description": "Создать макет с учетом нового брендбука",
            "priority": 3
        }
    """
    
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название задачи. Должно содержать от 3 до 100 символов.",
        examples=["Разработать дизайн главной страницы", "Написать тесты для API"]
    )
    
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Детальное описание задачи. Необязательное поле. Максимум 500 символов.",
        examples=["Создать макет главной страницы с учётом нового брендбука"]
    )
    
    priority: int = Field(
        ...,
        ge=1,
        le=5,
        description="Приоритет задачи. Значения: 1 - низший, 5 - высший.",
        examples=[1, 3, 5]
    )
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        """
        Проверяет, что название не состоит только из пробелов.
        
        Args:
            v (str): Название задачи
            
        Returns:
            str: Очищенное название
            
        Raises:
            ValueError: Если название состоит только из пробелов
        """
        cleaned = v.strip()
        if not cleaned:
            raise ValueError('Название не может состоять только из пробелов или быть пустым')
        return cleaned
    
    @validator('priority')
    def validate_priority(cls, v: int) -> int:
        """
        Проверяет, что приоритет находится в допустимом диапазоне.
        
        Args:
            v (int): Значение приоритета
            
        Returns:
            int: Проверенное значение приоритета
            
        Raises:
            ValueError: Если приоритет вне диапазона 1-5
        """
        if not 1 <= v <= 5:
            raise ValueError('Приоритет должен быть от 1 до 5')
        return v
    class Config:
        schema_extra = {
            "example": {
                "title": "Разработать дизайн главной страницы",
                "description": "Создать макет с учетом нового брендбука и цветовой схемы",
                "priority": 3
            }
        }


class TaskResponse(BaseModel):
    """
    Модель ответа с полными данными задачи.
    
    Возвращается при успешном создании задачи (POST /tasks) и при запросе
    задачи по идентификатору (GET /tasks/{task_id}).
    
    Включает все пользовательские поля и системные метаданные,
    автоматически добавляемые сервером.
    
    Attributes:
        id (str): Уникальный идентификатор задачи (UUID v4)
        title (str): Название задачи
        description (Optional[str]): Описание задачи
        priority (int): Приоритет задачи (1-5)
        created_at (datetime): Дата и время создания в формате UTC ISO 8601
    
    Example:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Разработать дизайн главной страницы",
            "description": "Создать макет с учетом нового брендбука",
            "priority": 3,
            "created_at": "2026-06-21T10:30:00.000Z"
        }
    """
    
    id: str = Field(
        ...,
        description="Уникальный идентификатор задачи в формате UUID версии 4.",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    
    title: str = Field(
        ...,
        description="Название задачи. Должно быть от 3 до 100 символов.",
        examples=["Разработать дизайн главной страницы"]
    )
    
    description: Optional[str] = Field(
        None,
        description="Детальное описание задачи. Необязательное поле.",
        examples=["Создать макет главной страницы с учётом нового брендбука"]
    )
    
    priority: int = Field(
        ...,
        description="Приоритет задачи от 1 (низший) до 5 (высший).",
        examples=[3]
    )
    
    created_at: datetime = Field(
        ...,
        description="Дата и время создания задачи в формате UTC (ISO 8601).",
        examples=["2026-06-21T10:30:00.000Z"]
    )
    
    class Config:
        """Конфигурация модели для сериализации"""
        json_encoders = {
            datetime: lambda v: v.isoformat() + 'Z'
        }
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Разработать дизайн главной страницы",
                "description": "Создать макет с учетом нового брендбука",
                "priority": 3,
                "created_at": "2026-06-21T10:30:00.000Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Модель стандартизированного ответа об ошибке.
    
    Используется для всех ошибок API для обеспечения единообразия
    и упрощения обработки ошибок на клиенте.
    
    Attributes:
        detail (str): Человекочитаемое описание ошибки
        status_code (int): HTTP статус-код ошибки
    
    Example:
        {
            "detail": "Задача с идентификатором 'invalid-id' не найдена",
            "status_code": 404
        }
    """
    
    detail: str = Field(
        ...,
        description="Подробное описание возникшей ошибки на русском языке.",
        examples=["Задача с указанным идентификатором не найдена"]
    )
    
    status_code: int = Field(
        ...,
        description="HTTP статус-код, соответствующий типу ошибки.",
        examples=[404, 422]
    )
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Задача с идентификатором '123' не найдена",
                "status_code": 404
            }
        }