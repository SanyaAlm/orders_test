from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.repositories.order_repo import OrderRepository
from app.application.services.order_service import OrderService
from app.application.users.transport import current_user
from app.domain.models import User
from app.infrastructure.db_connection import get_async_session
from app.presentation.mappers.order_mapper import (
    map_order_to_dto,
    map_order_create_dto_to_order,
    map_order_update_dto_to_order,
)
from app.presentation.schemas.order import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderUpdateDTO,
)

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
    user: User = Depends(current_user),
):
    user_id = user.id if not user.is_superuser else None

    orders = await service.get_orders(
        status=status, min_price=min_price, max_price=max_price, user_id=user_id
    )

    return [map_order_to_dto(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponseDTO)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return map_order_to_dto(order)


@router.post("/create", response_model=OrderResponseDTO)
async def create_order(
    order_dto: OrderCreateDTO,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    order = map_order_create_dto_to_order(order_dto)
    order.user_id = user.id
    created_order = await service.create_order(order)
    return map_order_to_dto(created_order)


@router.put("/update/{order_id}", response_model=OrderResponseDTO)
async def update_order(
    order_id: int,
    order_dto: OrderUpdateDTO,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    order = map_order_update_dto_to_order(order, order_dto)
    updated_order = await service.update_order(order)

    return map_order_to_dto(updated_order)


@router.delete("/delete/{order_id}", response_model=OrderResponseDTO)
async def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    order = await service.get_order_by_id(order_id=order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    deleted_order = await service.soft_delete_order(order)

    return map_order_to_dto(deleted_order)
