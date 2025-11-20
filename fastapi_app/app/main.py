from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.exceptions import exception_handler
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Starting FastAPI application")
    yield

    print("🛑 Shutting down FastAPI application")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Исключения
    app.add_exception_handler(500, exception_handler)

    # Роутеры
    app.include_router(api_router, prefix="/api/v1")

    # Корневой редирект
    @app.get("/")
    async def root():
        return RedirectResponse(url="/api/v1/emails/form")

    return app


app = create_app()