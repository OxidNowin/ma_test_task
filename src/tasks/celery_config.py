from celery import Celery
from celery.schedules import crontab

from config import settings


app = Celery(
    "ma_test_task",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

app.conf.beat_schedule = {
    "cleanup_files": {
        "task": "src.tasks.cleanup_files",
        "schedule": crontab(hour='6', minute='0'),
    },
}

app.conf.timezone = "Europe/Moscow"
