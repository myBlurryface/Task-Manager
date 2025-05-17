from django.urls import path

from .views import TasksCreateView, GetAndPatchSingleTaskView, GetListOfUsersTasksView

urlpatterns = [
    path("tasks/", GetListOfUsersTasksView.as_view(), name="get-list-of-tasks-by-tg-user-id"),
    path("tasks/", TasksCreateView.as_view(), name="operations-with-single-task"),
    path("tasks/<int:task_id>/", GetAndPatchSingleTaskView.as_view(), name="get-or-patch-single-task"),
]
