import fastapi

from app.application.users.transport import auth_backend, fastapi_users
from app.presentation.api.routers import api_router
from app.presentation.schemas.user import UserRead, UserCreate


app = fastapi.FastAPI()

app.include_router(
    api_router,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
