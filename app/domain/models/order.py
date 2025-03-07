import enum

from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models import Base


class OrderStatus(enum.Enum):
    """Перечисление для статусов заказа (pending, confirmed, cancelled)."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base):
    """Модель заказа с полями для статуса, общей стоимости, флага удаления, имени клиента, связи с пользователем и продуктами."""

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    total_price: Mapped[int]
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    products = relationship(
        "Product", back_populates="order", cascade="all, delete-orphan"
    )
