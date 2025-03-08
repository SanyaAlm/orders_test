from app.domain.models import Order
from app.domain.models.order import OrderStatus


async def test_get_order_by_id(get_test_session, login_admin_user):
    orders = [
        Order(
            customer_name="John1 Doe",
            total_price=100,
            status=OrderStatus.PENDING,
            user_id=1,
        ),
        Order(
            customer_name="Jane33",
            total_price=200,
            status=OrderStatus.CONFIRMED,
            user_id=1,
        ),
        Order(
            customer_name="Bob",
            total_price=300,
            status=OrderStatus.CANCELLED,
            user_id=1,
        ),
    ]

    async with get_test_session as session:
        session.add_all(orders)
        await session.commit()

    async_client, user = login_admin_user
    order_id = 1
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["customer_name"] == "John1 Doe"
    assert data["total_price"] == 100
    assert data["status"] == "pending"

    order_id = 2
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["customer_name"] == "Jane33"
    assert data["total_price"] == 200
    assert data["status"] == "confirmed"


async def test_get_order_by_non_existent_id(get_test_session, login_admin_user):
    async_client, user = login_admin_user
    order_id = 9999
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Order not found"
