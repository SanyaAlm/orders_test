from sqlalchemy.orm import Mapped

from app.domain.models import Base


class Product(Base):
    name: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]
