from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.application.repositories.base_repo import BaseRepository
from app.domain.models import Order


class OrderRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order) -> Order:
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

    async def get_by_id(self, order_id: int) -> Order:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.products))
            .where(Order.id == order_id, Order.is_deleted == False)
        )
        order = result.scalar_one_or_none()
        return order

    async def update(self, order: Order) -> Order:
        merged_order = await self.db.merge(order)
        await self.db.commit()
        await self.db.refresh(merged_order)
        return order

    async def delete(self, order: Order) -> Order:
        merged_order = await self.db.merge(order)
        await self.db.commit()
        await self.db.refresh(merged_order)
        return order

    async def get_all(self, filters: list):
        query = select(Order).options(selectinload(Order.products)).where(*filters)
        result = await self.db.execute(query)
        return result.scalars().all()
