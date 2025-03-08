import pytest


@pytest.mark.asyncio
async def test_delete_order(get_test_session, login_admin_user, create_orders):

    async_client, user = login_admin_user
    order_id = 1
    response = await async_client.delete(f"/orders/delete/{order_id}")

    assert response.status_code == 204

    response_after_delete = await async_client.get(f"/orders/{order_id}")

    assert response_after_delete.status_code == 404
    assert response_after_delete.json()["detail"] == "Order not found"


@pytest.mark.asyncio
async def test_delete_non_existent_order(get_test_session, login_admin_user):
    non_existent_order_id = 999
    async_client, user = login_admin_user
    response = await async_client.delete(f"/orders/delete/{non_existent_order_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
