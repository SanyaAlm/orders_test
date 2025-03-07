from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Создаёт новую сущность и возвращает её."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Возвращает сущность по её идентификатору или None, если не найдена."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Обновляет сущность и возвращает её."""
        pass

    @abstractmethod
    async def delete(self, entity: T) -> T:
        """Удаляет (или мягко удаляет) сущность и возвращает её."""
        pass

    @abstractmethod
    async def get_all(self, **filters) -> List[T]:
        """Возвращает список сущностей, удовлетворяющих фильтрам."""
        pass
