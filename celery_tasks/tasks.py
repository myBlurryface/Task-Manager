import pytz
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks_operator.models import UserTasks


@shared_task
def check_overdue_tasks():
    minsk_tz = pytz.timezone('Europe/Minsk')
    now = timezone.now().astimezone(minsk_tz)
    ten_minutes_later = now + timedelta(minutes=10)

    # Get tasks from database with status = True and deadline of + 10 minutes from now
    tasks = UserTasks.objects.filter(
        status=True,
        deadline__gte=now,
        deadline__lte=ten_minutes_later
    )

    for task in tasks:
        print("Сообщение отправлено ботом")

    print("Task finished tttttt")
