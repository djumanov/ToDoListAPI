from django.urls import path
from .views import (
    GetAllTasksView,
    GetTaskByIdView,
    AddTaskView,
)


urlpatterns = [
    path('tasks/', GetAllTasksView.as_view()),
    path('task/<int:id>', GetTaskByIdView.as_view()),
    path('add-task/', AddTaskView.as_view()),
]
