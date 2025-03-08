import pytest

from app.domain.models import Order
from app.domain.models.order import OrderStatus


@pytest.mark.asyncio
async def test_update_order_by_id(get_test_session, login_admin_user, create_orders):

    async_client, user = login_admin_user
    order_id = 1
    update_data = {
        "customer_name": "John Updated",
        "total_price": 150,
        "status": "confirmed",
        "products": [{"name": "string", "price": 75, "quantity": 2}],
    }

    response = await async_client.put(f"/orders/update/{order_id}", json=update_data)
    print(response.json())

    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["customer_name"] == update_data["customer_name"]
    assert updated_order["total_price"] == update_data["total_price"]
    assert updated_order["status"] == update_data["status"]


@pytest.mark.asyncio
async def test_update_order_not_found(get_test_session, login_admin_user):
    async_client, user = login_admin_user

    update_data = {
        "customer_name": "Non-existent Customer",
        "total_price": 500,
        "status": "pending",
        "products": [{"name": "string", "price": 75, "quantity": 2}],
    }

    response = await async_client.put("/orders/update/9999", json=update_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.asyncio
async def test_update_order_invalid_data(get_test_session, login_admin_user):
    # Создаем начальный заказ
    order = Order(
        customer_name="John1 Doe",
        total_price=101,
        status=OrderStatus.PENDING,
        user_id=1,
    )

    async with get_test_session as session:
        session.add(order)
        await session.commit()

    async_client, user = login_admin_user

    update_data = {
        "customer_name": "John Updated",
        "total_price": -10,
        "status": "INVALID_STATUS",
        "products": [{"name": "string", "price": 75, "quantity": 2}],
    }

    response = await async_client.put(f"/orders/update/{order.id}", json=update_data)

    assert response.status_code == 400
    assert "detail" in response.json()
