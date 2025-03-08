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
