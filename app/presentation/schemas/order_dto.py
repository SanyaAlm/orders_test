from pydantic import BaseModel, field_validator
from typing import List

from .product_dto import ProductDTO
from ...domain.models.order import OrderStatus


class OrderCreateDTO(BaseModel):
    customer_name: str
    status: str = "pending"
    products: List[ProductDTO]

    @field_validator("status")
    def check_status_validity(cls, v):
        if v not in OrderStatus.__members__:
            raise ValueError(f"'{v}' is not a valid OrderStatus")
        return OrderStatus[v]


class OrderUpdateDTO(BaseModel):
    customer_name: str
    status: str
    products: List[ProductDTO]


class OrderResponseDTO(BaseModel):
    order_id: int
    customer_name: str
    status: str
    total_price: int
    products: List[ProductDTO]
