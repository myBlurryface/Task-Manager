from django.urls import path

from .views import TasksCreateOrGetListOfTasksView, GetAndPatchSingleTaskView

urlpatterns = [
    path("tasks/", TasksCreateOrGetListOfTasksView.as_view(), name="operations-with-single-task"),
    path("tasks/<int:task_id>/", GetAndPatchSingleTaskView.as_view(), name="get-or-patch-single-task"),
]
