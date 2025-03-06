from pydantic import BaseModel
from typing import List


class ProductDTO(BaseModel):
    name: str
    price: int
    quantity: int


class OrderCreateDTO(BaseModel):
    customer_name: str
    status: str = "pending"
    products: List[ProductDTO]


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
