from celery import Celery
from app.core.config import settings


def create_celery_app() -> Celery:
    celery_app = Celery(
        'fastapi_worker',
        broker=settings.redis_url,
        backend=settings.redis_url,
        include=['app.services.tasks']
    )

    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,
    )

    return celery_app


celery_app = create_celery_app()