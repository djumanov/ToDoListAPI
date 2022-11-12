from django.urls import path
from .views import (
    GetAllTasksView,
    GetTaskByIdView,
)


urlpatterns = [
    path('tasks/', GetAllTasksView.as_view()),
    path('task/<int:id>', GetTaskByIdView.as_view()),
]
