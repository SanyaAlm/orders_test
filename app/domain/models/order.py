import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models import Base


class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base):
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    total_price: Mapped[int]
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)

    products = relationship(
        "Product", back_populates="order", cascade="all, delete-orphan"
    )
