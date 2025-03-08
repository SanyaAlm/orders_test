import pytest


@pytest.mark.asyncio
async def test_create_order(login_admin_user):
    """Тест на создание нового заказа."""
    order_data = {
        "customer_name": "John Doe",
        "status": "pending",
        "products": [
            {"name": "Laptop", "price": 1000, "quantity": 1},
            {"name": "Mouse", "price": 50, "quantity": 2},
        ],
    }

    async_client, user = login_admin_user
    response = await async_client.post("/orders/create", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "pending"
    assert data["total_price"] == 1100
    assert len(data["products"]) == 2


@pytest.mark.asyncio
async def test_create_wrong_order(login_admin_user):
    """Тест на создание нового заказа с ошибкой"""
    order_data = {
        "customer_name": "John Doe",
        "status": "new",
        "products": [
            {"name": "Laptop", "price": 1000, "quantity": 1},
            {"name": "Mouse", "price": 50, "quantity": 2},
        ],
    }

    async_client, user = login_admin_user
    response = await async_client.post("/orders/create", json=order_data)

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


# async def test_redis_cache(login_admin_user, get_test_redis):
#     """Тест на создание нового заказа."""
#     redis = get_test_redis
#     print(redis)
#     order_data = {
#         "customer_name": "John D",
#         "status": "pending",
#         "products": [
#             {"name": "Laptop", "price": 1000, "quantity": 1},
#         ],
#     }
#     async_client, user = login_admin_user
#     response = await async_client.post("/orders/create", json=order_data)
#     assert response.status_code == 201
#     data = response.json()
#     print(data, "DATAA")
#     cached_data = await redis.get(f"order:{data['order_id']}")
#     print(cached_data, "data")
#     assert cached_data is not None
#     cached_data = cached_data.decode("utf-8")
#     assert "John D" in cached_data
