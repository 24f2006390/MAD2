from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "myapp", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1"
)

celery.conf.timezone = "Asia/Kolkata"

from celery_tasks import tasks

celery.conf.beat_schedule = {
    "print-every-minute": {
        "task": "celery_tasks.tasks.send_daily_emails",
        "schedule": crontab(hour=6,minute=0),
    },
    "Monthy-admin-report": {
        "task": "celery_tasks.tasks.send_admin_report",
        "schedule": crontab( day_of_month=1,hour=0,minute=0 ),
    },
}

# cd backend
# celery -A celery_tasks.celery_app.celery worker --loglevel=info
# celery -A celery_tasks.celery_app.celery beat --loglevel=info
