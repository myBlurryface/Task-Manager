from django.db import models


class UserTasks(models.Model):
    tg_user_id = models.BigIntegerField(null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    deadline = models.DateTimeField(blank=False, null=False)
    status = models.BooleanField(default=True)
