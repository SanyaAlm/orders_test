from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/all", response_model=List[OrderResponseDTO])
async def get_orders(
    status: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    service: OrderService = Depends(get_order_service),
):
    orders = await service.get_orders(status, min_price, max_price)
    return [map_order_to_dto(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponseDTO)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return map_order_to_dto(order)


@router.post("/create", response_model=OrderResponseDTO)
async def create_order(
    order_dto: OrderCreateDTO, service: OrderService = Depends(get_order_service)
):
    order = map_order_create_dto_to_order(order_dto)
    created_order = await service.create_order(order)
    return map_order_to_dto(created_order)
