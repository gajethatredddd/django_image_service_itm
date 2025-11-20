from fastapi import Depends
from app.services.django_client import DjangoClient
from app.services.email_service import EmailService
from app.core.celery import celery_app
from app.core.config import settings

async def get_django_client() -> DjangoClient:
    return DjangoClient(settings.django_api_url)

async def get_email_service() -> EmailService:
    return EmailService()

async def get_celery_app():
    return celery_app