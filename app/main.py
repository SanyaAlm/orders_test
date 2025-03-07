import fastapi

from app.presentation.api.routers import api_router


app = fastapi.FastAPI()

app.include_router(
    api_router,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
