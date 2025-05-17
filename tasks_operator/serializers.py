import datetime

from rest_framework import serializers
from django.utils import timezone

from .models import UserTasks


class TaskCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTasks
        fields = (
            "tg_user_id",
            "title",
            "description",
            "deadline",
        )

        def validate(self, data) -> dict:
            deadline = data.get('deadline')

            if deadline:
                min_allowed_deadline = timezone.now() + datetime.timedelta(minutes=1)
                if deadline < min_allowed_deadline:
                    raise serializers.ValidationError(
                        {"deadline": "Deadline must be at least 10 minutes later from now."}
                    )
            return data


class TasksResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTasks
        fields = '__all__'


class GetUserTasksListSerializer(serializers.Serializer):
    telegram_user_id = serializers.IntegerField(required=True)


class TaskStatusSerializer(serializers.Serializer):
    task_status = serializers.BooleanField(required=True, allow_null=False)
