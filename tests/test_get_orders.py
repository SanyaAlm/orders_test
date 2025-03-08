from app.domain.models import Order
from app.domain.models.order import OrderStatus


async def test_get_all_orders(login_admin_user, get_test_session):
    orders = [
        Order(
            customer_name="John", total_price=100, status=OrderStatus.PENDING, user_id=1
        ),
        Order(
            customer_name="Jane",
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
    response = await async_client.get("/orders/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["status"] == "pending"
    assert data[1]["status"] == "confirmed"
    assert data[2]["status"] == "cancelled"


async def test_get_orders_by_status(login_admin_user, get_test_session):
    orders = [
        Order(
            customer_name="John Doe",
            total_price=100,
            status=OrderStatus.PENDING,
            user_id=1,
        ),
        Order(
            customer_name="Jane",
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
    response = await async_client.get("/orders/all?status=confirmed")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "confirmed"


async def test_get_orders_for_user(login_regular_user, get_test_session):
    # Создаем заказы для разных пользователей
    orders = [
        Order(
            customer_name="John", total_price=100, status=OrderStatus.PENDING, user_id=1
        ),
        Order(
            customer_name="Jane",
            total_price=200,
            status=OrderStatus.CONFIRMED,
            user_id=2,
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

    async_client, user = login_regular_user
    response = await async_client.get("/orders/all")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["customer_name"] == "John"
    assert data[1]["customer_name"] == "Bob"
