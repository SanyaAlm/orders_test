from pydantic import BaseModel


class ProductDTO(BaseModel):
    name: str
    price: int
    quantity: int
