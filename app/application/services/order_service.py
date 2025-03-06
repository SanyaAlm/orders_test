from typing import Optional, List

from app.application.repositories.order_repo import OrderRepository
from app.domain.models import Order
from app.domain.models.order import OrderStatus


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def create_order(self, order: Order) -> Order:
        order.total_price = sum(p.price * p.quantity for p in order.products)
        return await self.repository.create_order(order)

    async def update_order(self, order: Order) -> Order:
        order.total_price = sum(p.price * p.quantity for p in order.products)
        return await self.repository.update_order(order)

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return await self.repository.get_order_by_id(order_id)

    async def get_orders(
        self,
        status: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[Order]:
        enum_status = OrderStatus(status) if status else None
        return await self.repository.get_orders(
            status=enum_status, min_price=min_price, max_price=max_price
        )

    async def soft_delete_order(self, order: Order) -> Order:
        return await self.repository.soft_delete_order(order)
