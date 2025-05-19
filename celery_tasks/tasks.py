import os
import pytz
import requests

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks_operator.models import UserTasks
from dotenv import load_dotenv
from tasks_operator.serializers import TasksResponseSerializer

load_dotenv()

DJANGO_SECRET_TOKEN = os.getenv("DJANGO_SECRET_TOKEN", "")
BOT_WEBHOOK_URL = os.getenv("BOT_WEBHOOK_URL")
HEADERS = {"X-Django-Secret-Token": DJANGO_SECRET_TOKEN}


@shared_task
def check_overdue_tasks():
    minsk_tz = pytz.timezone('Europe/Minsk')
    now = timezone.now().astimezone(minsk_tz)
    ten_minutes_later = now + timedelta(minutes=10)

    # Get tasks from database with status = True and deadline of + 10 minutes from now
    tasks_list = UserTasks.objects.filter(
       status=True,
       deadline__gte=now,
       deadline__lte=ten_minutes_later
    )

    if tasks_list.exists():
        tasks_list_serialized = TasksResponseSerializer(tasks_list, many=True)
        response = requests.post(BOT_WEBHOOK_URL, json=tasks_list_serialized.data, headers=HEADERS)
        print(response.content)
    else:
        print("No tasks found")
