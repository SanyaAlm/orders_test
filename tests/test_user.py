import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_regular_user(async_client: AsyncClient, test_regular_user):
    """Тест на логин обычного пользователя."""
    client_data = {
        "username": test_regular_user.email,
        "password": "123",
        "grant_type": "password",
    }

    # Пытаемся выполнить логин с правильными данными
    response = await async_client.post("/auth/login", data=client_data)

    assert response.status_code == 200
    assert "access_token" in response.json(), "Access token should be returned"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient, test_regular_user):
    """Тест на логин с неверными данными."""
    client_data = {
        "username": test_regular_user.email,
        "password": "wrongpassword",  # Неверный пароль
        "grant_type": "password",
    }

    response = await async_client.post("/auth/login", data=client_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"


@pytest.mark.asyncio
async def test_login_non_existent_user(async_client: AsyncClient):
    """Тест на логин с несуществующим пользователем."""
    client_data = {
        "username": "nonexistent_user@gmail.com",  # Не существующий пользователь
        "password": "123",
        "grant_type": "password",
    }

    response = await async_client.post("/auth/login", data=client_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
