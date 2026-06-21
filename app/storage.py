from typing import Dict, Optional, List
from datetime import datetime
import uuid
from app.models import TaskCreate, TaskResponse


class TaskStorage:
    """
    Временное хранилище задач в оперативной памяти.
    
    Используется для демонстрационных целей вместо базы данных.
    Данные теряются при перезапуске приложения.
    """
    
    def __init__(self):
        """Инициализирует пустое хранилище задач."""
        self._tasks: Dict[str, TaskResponse] = {}
    
    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """
        Создает новую задачу и сохраняет её в хранилище.
        
        Args:
            task_data (TaskCreate): Данные для создания задачи
            
        Returns:
            TaskResponse: Созданная задача с системными полями
        """
        task_id = str(uuid.uuid4())
        task = TaskResponse(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            created_at=datetime.utcnow()
        )
        self._tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[TaskResponse]:
        """
        Получает задачу по идентификатору.
        
        Args:
            task_id (str): Уникальный идентификатор задачи
            
        Returns:
            Optional[TaskResponse]: Задача, если найдена, иначе None
        """
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[TaskResponse]:
        """
        Получает список всех задач.
        
        Returns:
            List[TaskResponse]: Список всех задач в хранилище
        """
        return list(self._tasks.values())
    
    def delete_task(self, task_id: str) -> bool:
        """
        Удаляет задачу по идентификатору.
        
        Args:
            task_id (str): Уникальный идентификатор задачи
            
        Returns:
            bool: True если задача удалена, False если не найдена
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def update_task(self, task_id: str, task_data: TaskCreate) -> Optional[TaskResponse]:
        """
        Полностью обновляет задачу.
        
        Args:
            task_id (str): Уникальный идентификатор задачи
            task_data (TaskCreate): Новые данные для задачи
            
        Returns:
            Optional[TaskResponse]: Обновленная задача или None если не найдена
        """
        if task_id not in self._tasks:
            return None
        
        task = self._tasks[task_id]
        updated_task = TaskResponse(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            created_at=task.created_at  # Сохраняем оригинальную дату создания
        )
        self._tasks[task_id] = updated_task
        return updated_task
    
    def partial_update_task(self, task_id: str, task_data: TaskCreate) -> Optional[TaskResponse]:
        """
        Частично обновляет задачу.
        
        Args:
            task_id (str): Уникальный идентификатор задачи
            task_data (TaskCreate): Данные для обновления
            
        Returns:
            Optional[TaskResponse]: Обновленная задача или None если не найдена
        """
        if task_id not in self._tasks:
            return None
        
        existing_task = self._tasks[task_id]
        updated_task = TaskResponse(
            id=task_id,
            title=task_data.title if task_data.title else existing_task.title,
            description=task_data.description if task_data.description is not None else existing_task.description,
            priority=task_data.priority if task_data.priority else existing_task.priority,
            created_at=existing_task.created_at
        )
        self._tasks[task_id] = updated_task
        return updated_task
    
    def clear(self) -> None:
        """
        Очищает хранилище, удаляя все задачи.
        """
        self._tasks.clear()