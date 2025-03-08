from app.domain.models import Order
from app.domain.models.order import OrderStatus


async def test_delete_order(get_test_session, login_admin_user):
    orders = [
        Order(
            customer_name="John1 Doe",
            total_price=102,
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
    response = await async_client.delete(f"/orders/delete/{order_id}")

    assert response.status_code == 204

    response_after_delete = await async_client.get(f"/orders/{order_id}")

    assert response_after_delete.status_code == 404
    assert response_after_delete.json()["detail"] == "Order not found"


async def test_delete_non_existent_order(get_test_session, login_admin_user):
    non_existent_order_id = 999
    async_client, user = login_admin_user
    response = await async_client.delete(f"/orders/delete/{non_existent_order_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
