import os
from celery import Celery
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "image_service.settings")
django.setup()

app = Celery("image_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
