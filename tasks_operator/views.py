from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema

from .models import UserTasks
from .serializers import (
    TaskCreationSerializer,
    TasksResponseSerializer,
    GetUserTasksListSerializer,
    TaskStatusSerializer,
)


class TasksCreateOrGetListOfTasksView(APIView):

    @extend_schema(
        tags=["Single task operations"],
        summary="Create a new task for a user",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "tg_user_id": {
                        "type": "integer",
                        "example": 4544456767778,
                        "description": "Telegram user id",
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 255,
                        "example": "Call me later.",
                        "description": "Title of the task."
                    },
                    "description": {
                        "type": "string",
                        "maxLength": 500,
                        "example": "This task reminds me to call someone later.",
                        "description": "Description of the task."
                    },
                    "deadline": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2025-05-17T12:00:00Z",
                        "description": "Description of the task."
                    },

                },
            }
        },
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "info": {"type": "string"},
                        "task_id": {"type": "integer"}
                    }
                },
                description="Task created successfully",
                examples=[
                    OpenApiExample(
                        "Successful creation",
                        value={"info": "Task created successfully", "task_id": 1}
                    )
                ]
            ),
            400: OpenApiResponse(
                response={"type": "object", "properties": {"Error": {"type": "string"}}},
                description="Invalid input",
                examples=[
                    OpenApiExample(
                        "Validation error",
                        value={"Error": "Deadline must be at least 10 minutes later from now."}
                    ),
                    OpenApiExample(
                        "General type error",
                        value={"Error": "Error creating task."}
                    )
                ],
            )
        }
    )
    def post(self, request: Request) -> Response:
        data_serializer = TaskCreationSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)

        task = data_serializer.validated_data
        try:
            created_task = UserTasks.objects.create(**task)
            return Response(
                data={
                    "info": "Task created successfully.",
                    "task_id": created_task.id
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Group if tasks operations"],
        summary="Get list of users tasks by tg_user_id",
        parameters=[
            OpenApiParameter(
                name="telegram_user_id",
                description="Specify filter for database for telegram user id. ",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        name="Telegram user id",
                        description="Retrieve templates for user with this telegram id.",
                        value=4456588577
                    ),
                ]
            )
        ],
        responses={
            200: OpenApiResponse(
                response=list[dict],
                description="Returns all tasks for specified user.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        [
                            {
                                "tg_user_id": "4456588577",
                                "title": "Call me later.",
                                "description": "This task reminds me to call someone later.",
                                "deadline": "2025-05-17T12:00:00Z",
                                "status": True,
                            },
                            {
                                "tg_user_id": "4456588577",
                                "title": "Call me later, Sally.",
                                "description": "This task reminds me, that Sally should call me later.",
                                "deadline": "2025-05-18T12:00:00Z",
                                "status": True,
                            },
                        ]
                    )
                ],
            ),
            400: OpenApiResponse(
                response=dict,
                description="Additional errors, that can occur during operations with database.",
                examples=[
                    OpenApiExample(
                        "General type error",
                        value={"Error": "Error getting list of tasks"}
                    )
                ],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        serializer = GetUserTasksListSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        tg_user_id = serializer.validated_data.get("telegram_user_id")

        try:
            tasks_list = UserTasks.objects.filter(tg_user_id=tg_user_id)
            response_tasks_list = TasksResponseSerializer(tasks_list, many=True)
            return Response(response_tasks_list.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAndPatchSingleTaskView(APIView):

    @extend_schema(
        tags=["Single task operations"],
        summary="Get a single task by ID",
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "tg_user_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "deadline": {"type": "string"},
                        "status": {"type": "boolean"},
                    }
                },
            ),
            400: OpenApiResponse(
                response=dict,
                description="Additional errors, that can occur during operations with database.",
                examples=[
                    OpenApiExample(
                        "General type error",
                        value={"Error": "Error getting list of tasks"}
                    )
                ],
            ),
        }
    )
    @extend_schema(tags=["Single task operations"], summary="Get single task by task_id")
    def get(self, request: Request, task_id: int) -> Response:
        try:
            task = UserTasks.objects.get(id=task_id)
            response_data = TasksResponseSerializer(task)
            return Response(response_data.data, status=status.HTTP_201_CREATED)
        except UserTasks.DoesNotExist:
            return Response(
                data={"error": f"Task with id={task_id} not found."},
                status=status.HTTP_404_NOT_FOUND
           )

    @extend_schema(
        tags=["Single task operations"],
        summary="Change task status",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "task_status": {
                        "type": "boolean",
                        "example": True,
                        "description": "Task status to be set.",
                    },
                },
            }
        },
        responses={
            200: OpenApiResponse(
                response={
                    "type": "string",
                },
                description="Task status updated successfully",
                examples=[
                    OpenApiExample(
                        "Status updated",
                        value="Task with id = 1 now done"
                    )
                ]
            ),
            400: OpenApiResponse(
                response=dict,
                description="Additional errors, that can occur during operations with database.",
                examples=[
                    OpenApiExample(
                        "General type error",
                        value={"Error": "Error getting list of tasks"}
                    )
                ],
            ),
        }
    )
    def patch(self, request: Request, task_id: int) -> Response:
        serialized_data = TaskStatusSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        task_status = serialized_data.validated_data.get("task_status")
        try:
            task = UserTasks.objects.get(id=task_id)
            task.status = task_status
            task.save()
            text_task_status = "done" if task.status is False else "undone"
            return Response(data=f"Task with id = {task.id} now {text_task_status}.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
