from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.domain.models import Base


class Product(Base):
    """Модель продукта, входящего в заказ, с полями для названия, цены, количества и ссылкой на заказ."""

    name: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    order = relationship("Order", back_populates="products")
