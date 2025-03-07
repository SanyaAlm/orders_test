from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models import Order
from app.domain.models.order import OrderStatus


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)

        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.products))
            .where(Order.id == order.id)
        )
        order = result.scalar_one()

        return order

    async def get_order_by_id(self, order_id: int) -> Order:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.products))
            .where(Order.id == order_id, Order.is_deleted == False)
        )
        order = result.scalar_one_or_none()
        return order

    async def update_order(self, order: Order) -> Order:
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def soft_delete_order(self, order: Order) -> Order:
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get_orders(self, filters: list):
        query = select(Order).options(selectinload(Order.products)).where(*filters)
        result = await self.db.execute(query)
        return result.scalars().all()
