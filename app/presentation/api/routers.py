from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.application.users.transport import fastapi_users, auth_backend
from app.presentation.api.endpoints import order
from app.presentation.schemas.user_dto import UserRead, UserCreate

http_bearer: HTTPBearer = HTTPBearer(auto_error=False)

api_router = APIRouter(dependencies=[Depends(http_bearer)])

api_router.include_router(order.router, prefix="/orders", tags=["order"])

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
