from django.urls import path
from .views import (
    GetAllTasksView,
)


urlpatterns = [
    path('tasks/', GetAllTasksView.as_view()),
]
