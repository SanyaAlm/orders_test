from typing import Optional, List, Any, Coroutine

from app.application.repositories.order_repo import OrderRepository
from app.domain.models import Order
from app.domain.models.order import OrderStatus
from app.infrastructure.logging import logger
from app.infrastructure.redis_cache import (
    set_order_cache,
    delete_order_cache,
    get_order_cache,
)
from app.presentation.mappers.order_mapper import (
    map_order_to_cache_data,
    map_cache_to_order,
)


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def create_order(self, order: Order) -> Order:
        """Создает заказ, вычисляет его общую стоимость, сохраняет в БД, кэширует и логирует создание."""
        order.total_price = sum(p.price * p.quantity for p in order.products)
        created_order = await self.repository.create(order)
        order_data = map_order_to_cache_data(created_order)
        logger.info(f"User {created_order.user_id} created order {created_order.id}")
        await set_order_cache(created_order.id, order_data)

        return created_order

    async def update_order(self, order: Order) -> Order:
        """Обновляет заказ, пересчитывает его общую стоимость, сохраняет изменения, обновляет кэш и логирует обновление."""
        order.total_price = sum(p.price * p.quantity for p in order.products)
        updated_order = await self.repository.update(order)
        order_data = map_order_to_cache_data(updated_order)
        logger.info(f"User {updated_order.user_id} updated order {updated_order.id}")
        await set_order_cache(updated_order.id, order_data)

        return updated_order

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Получает заказ по идентификатору, кэширует его данные и возвращает заказ, если он найден."""
        cached_data = await get_order_cache(order_id)
        if cached_data:
            # Если данные найдены в кэше, мапим их в объект заказа
            return map_cache_to_order(cached_data)
        order = await self.repository.get_by_id(order_id)
        if order:
            order_data = map_order_to_cache_data(order)
            await set_order_cache(order.id, order_data)
        return order

    async def get_orders(
        self,
        user_id: int,
        status: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ):
        """Возвращает список заказов, отфильтрованных по пользователю, статусу и диапазону цен."""
        enum_status = OrderStatus(status) if status else None
        filters = [Order.is_deleted == False]
        if user_id:
            filters.append(Order.user_id == user_id)
        if status:
            filters.append(Order.status == enum_status)
        if min_price:
            filters.append(Order.total_price >= min_price)
        if max_price:
            filters.append(Order.total_price <= max_price)

        return await self.repository.get_all(filters)

    async def soft_delete_order(self, order: Order) -> Order:
        """Мягко удаляет заказ, устанавливая флаг удаления, удаляет его из кэша и логирует событие."""
        order.is_deleted = True
        deleted_order = await self.repository.delete(order)
        await delete_order_cache(deleted_order.id)
        logger.info(f"User {deleted_order.user_id} deleted order {deleted_order.id}")

        return deleted_order
