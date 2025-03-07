from typing import Optional, List

from app.application.repositories.order_repo import OrderRepository
from app.domain.models import Order
from app.domain.models.order import OrderStatus
from app.infrastructure.redis_cache import (
    set_order_cache,
    delete_order_cache,
)
from app.presentation.mappers.order_mapper import map_order_to_cache_data


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def create_order(self, order: Order) -> Order:
        order.total_price = sum(p.price * p.quantity for p in order.products)
        created_order = await self.repository.create_order(order)
        order_data = map_order_to_cache_data(created_order)
        await set_order_cache(created_order.id, order_data)

        return created_order

    async def update_order(self, order: Order) -> Order:
        order.total_price = sum(p.price * p.quantity for p in order.products)
        updated_order = await self.repository.update_order(order)
        order_data = map_order_to_cache_data(updated_order)
        await set_order_cache(updated_order.id, order_data)

        return updated_order

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        order = await self.repository.get_order_by_id(order_id)
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
    ) -> List[Order]:
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

        return await self.repository.get_orders(filters)

    async def soft_delete_order(self, order: Order) -> Order:
        order.is_deleted = True
        deleted_order = await self.repository.soft_delete_order(order)
        await delete_order_cache(deleted_order.id)

        return deleted_order
