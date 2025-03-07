from app.domain.models import Order, Product
from app.domain.models.order import OrderStatus
from app.presentation.schemas.order_dto import (
    OrderResponseDTO,
    ProductDTO,
    OrderCreateDTO,
    OrderUpdateDTO,
)


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
        status=OrderStatus(dto.status),
    )
    for prod in dto.products:
        product = Product(name=prod.name, price=prod.price, quantity=prod.quantity)
        order.products.append(product)
    return order


def map_order_update_dto_to_order(order: Order, dto: OrderUpdateDTO) -> Order:
    order.customer_name = dto.customer_name
    order.status = OrderStatus(dto.status)
    order.products.clear()
    for prod in dto.products:
        product = Product(name=prod.name, price=prod.price, quantity=prod.quantity)
        order.products.append(product)
    return order


def map_order_to_cache_data(order: Order) -> dict:
    return {
        "order_id": order.id,
        "customer_name": order.customer_name,
        "status": order.status.value,
        "total_price": order.total_price,
        "user_id": order.user_id,
        "products": [
            {"name": p.name, "price": p.price, "quantity": p.quantity}
            for p in order.products
        ],
    }
