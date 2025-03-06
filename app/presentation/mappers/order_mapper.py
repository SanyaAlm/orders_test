from app.domain.models import Order, Product
from app.domain.models.order import OrderStatus
from app.presentation.schemas.order import OrderResponseDTO, ProductDTO, OrderCreateDTO


def map_order_to_dto(order: Order) -> OrderResponseDTO:
    products = [
        ProductDTO(name=p.name, price=p.price, quantity=p.quantity)
        for p in order.products
    ]
    return OrderResponseDTO(
        order_id=order.id,
        customer_name=order.customer_name,
        status=order.status.value,
        total_price=order.total_price,
        products=products,
    )


def map_order_create_dto_to_order(dto: OrderCreateDTO) -> Order:
    order = Order(
        customer_name=dto.customer_name,
        status=OrderStatus(dto.status),  # Преобразуем строку в Enum
    )
    for prod in dto.products:
        product = Product(name=prod.name, price=prod.price, quantity=prod.quantity)
        order.products.append(product)
    return order
