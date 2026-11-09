from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
# Finds tasks in app/tasks.py once you create it.
celery_app.autodiscover_tasks(["app"])
