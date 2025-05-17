import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

app = Celery('task_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['celery_tasks.tasks'])

app.conf.beat_schedule = {
    'check-tasks-every-minute': {
        'task': 'celery_tasks.tasks.check_overdue_tasks',
        'schedule': crontab(minute='*'),
    },
}