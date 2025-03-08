import pytest


@pytest.mark.asyncio
async def test_get_order_by_id(get_test_session, login_admin_user, create_orders):
    """Тест на получения заказа по его id"""
    async_client, user = login_admin_user
    order_id = 2
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()
    print(data)

    assert data["customer_name"] == "Jane33"
    assert data["total_price"] == 200
    assert data["status"] == "confirmed"

    order_id = 2
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["customer_name"] == "Jane33"
    assert data["total_price"] == 200
    assert data["status"] == "confirmed"


@pytest.mark.asyncio
async def test_get_order_by_non_existent_id(get_test_session, login_admin_user):
    """Тест на получения заказа по его id"""
    async_client, user = login_admin_user
    order_id = 9999
    response = await async_client.get(f"/orders/{order_id}")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Order not found"
