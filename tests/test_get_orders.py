import pytest


@pytest.mark.asyncio
async def test_get_all_orders(login_admin_user, get_test_session, create_orders):
    """Тест на получение всех заказов юзера"""
    async_client, user = login_admin_user
    response = await async_client.get("/orders/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    assert data[0]["status"] == "pending"
    assert data[1]["status"] == "confirmed"
    assert data[2]["status"] == "cancelled"


@pytest.mark.asyncio
async def test_get_orders_by_status(login_admin_user, get_test_session, create_orders):
    """Тест на получение всех заказов юзера с ошибкой"""
    async_client, user = login_admin_user
    response = await async_client.get("/orders/all?status=confirmed")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "confirmed"


@pytest.mark.asyncio
async def test_get_orders_for_user(login_regular_user, get_test_session, create_orders):
    """Тест на получение всех заказов обычного юзера"""
    async_client, user = login_regular_user
    response = await async_client.get("/orders/all")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
    assert data[0]["customer_name"] == "John Doe"
    assert data[1]["customer_name"] == "Jane33"
