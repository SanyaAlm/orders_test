from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.repositories.order_repo import OrderRepository
from app.application.services.order_service import OrderService
from app.core.security import current_user
from app.domain.models import User
from app.infrastructure.db_connection import get_async_session
from app.presentation.mappers.order_mapper import (
    map_order_to_dto,
    map_order_create_dto_to_order,
    map_order_update_dto_to_order,
)
from app.presentation.schemas.order_dto import (
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


@router.get(
    "/all",
    response_model=List[OrderResponseDTO,],
    summary="Эндпоинт возвращает список заявок",
    description="Обычный пользователь видит только свои заявки, администратор — все заявки.",
    status_code=status.HTTP_200_OK,
)
async def get_orders(
    status: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    """
    Получить список заявок с возможностью фильтрации по статусу и цене.
    - **status**: Фильтрация по статусу заявки (например, "pending", "confirmed", "cancelled").
    - **min_price**: Минимальная общая стоимость заявки.
    - **max_price**: Максимальная общая стоимость заявки.
    - **user**: Текущий авторизованный пользователь.
    Если пользователь не является администратором, возвращаются только его заявки.
    """
    user_id = user.id if not user.is_superuser else None

    orders = await service.get_orders(
        status=status, min_price=min_price, max_price=max_price, user_id=user_id
    )

    return [map_order_to_dto(order) for order in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponseDTO,
    summary="Эндроинт возвращает заявку по id",
    description="Возвращает информацию о заявке по заданному идентификатору. Доступно только владельцу заявки или администратору.",
    status_code=status.HTTP_200_OK,
)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    """
    Получить заявку по ее идентификатору.
    - **order_id**: Идентификатор заявки.
    - **user**: Текущий авторизованный пользователь.
    Если заявка не найдена, возвращается ошибка 404.
    Если пользователь не является администратором и не является владельцем заявки, возвращается ошибка 403.
    """
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return map_order_to_dto(order)


@router.post(
    "/create",
    response_model=OrderResponseDTO,
    summary="Эндпоинт для создания заявки",
    description="Эндпоинт для создания новой заявки. При создании заявка привязывается к текущему пользователю.",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_dto: OrderCreateDTO,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    """
    Создать новую заявку.
    - **order_dto**: Данные для создания заявки.
    - **user**: Текущий авторизованный пользователь.
    Созданная заявка будет привязана к идентификатору текущего пользователя.
    """
    try:
        order = map_order_create_dto_to_order(order_dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    order.user_id = user.id
    created_order = await service.create_order(order)
    return map_order_to_dto(created_order)


@router.put(
    "/update/{order_id}",
    response_model=OrderResponseDTO,
    summary="Эндпоинт для обновления заявки по id",
    description="Обновление данных существующей заявки. Доступно только владельцу заявки или администратору.",
    status_code=status.HTTP_200_OK,
)
async def update_order(
    order_id: int,
    order_dto: OrderUpdateDTO,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    """
    Обновить заявку по ее идентификатору.

    - **order_id**: Идентификатор заявки для обновления.
    - **order_dto**: Новые данные для обновления заявки.
    - **user**: Текущий авторизованный пользователь.

    Если заявка не найдена, возвращается ошибка 404.
    Если пользователь не имеет доступа к заявке, возвращается ошибка 403.
    """
    order = await service.get_order_by_id(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        order = map_order_update_dto_to_order(order, order_dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    updated_order = await service.update_order(order)

    return map_order_to_dto(updated_order)


@router.delete(
    "/delete/{order_id}",
    summary="Удалить заявку",
    description="Мягкое удаление заявки. Доступно только владельцу заявки или администратору.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(current_user),
):
    """
    Мягко удалить заявку по ее идентификатору.

    - **order_id**: Идентификатор заявки.
    - **user**: Текущий авторизованный пользователь.

    Если заявка не найдена, возвращается ошибка 404.
    Если пользователь не имеет доступа к заявке, возвращается ошибка 403.
    """

    order = await service.get_order_by_id(order_id=order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_superuser and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    await service.soft_delete_order(order)
