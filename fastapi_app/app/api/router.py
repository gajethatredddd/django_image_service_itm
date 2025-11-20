from fastapi import APIRouter
from app.api.routes import emails, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])