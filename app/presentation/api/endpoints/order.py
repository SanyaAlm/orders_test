from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.repositories.order_repo import OrderRepository
from app.application.services.order_service import OrderService
from app.infrastructure.db_connection import get_async_session
from app.presentation.mappers.order_mapper import (
    map_order_to_dto,
    map_order_create_dto_to_order,
)
from app.presentation.schemas.order import OrderCreateDTO, OrderResponseDTO

router = APIRouter()


async def get_order_service(
    db: AsyncSession = Depends(get_async_session),
) -> OrderService:
    repository = OrderRepository(db)
    return OrderService(repository)


@router.post("/orders", response_model=OrderResponseDTO)
async def create_order(
    order_dto: OrderCreateDTO, service: OrderService = Depends(get_order_service)
):
    order = map_order_create_dto_to_order(order_dto)
    created_order = await service.create_order(order)
    return map_order_to_dto(created_order)
