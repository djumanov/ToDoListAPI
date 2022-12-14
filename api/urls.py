from django.urls import path
from .views import (
    GetAllTasksView,
    GetTaskByIdView,
    AddTaskView,
    EditTaskView,
    DoneTaskView,
    GetAllCompletedTasksView,
    GetAllInCompletedTasksView,
)


urlpatterns = [
    path('tasks/', GetAllTasksView.as_view()),
    path('task/<int:id>', GetTaskByIdView.as_view()),
    path('add-task/', AddTaskView.as_view()),
    path('edit-task/<int:id>', EditTaskView.as_view()),
    path('done-task/<int:id>', DoneTaskView.as_view()),
    path('completed-tasks/', GetAllCompletedTasksView.as_view()),
    path('incompleted-tasks/', GetAllInCompletedTasksView.as_view()),
]
