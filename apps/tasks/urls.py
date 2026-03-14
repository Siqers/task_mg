from django.urls import path

from apps.tasks.views import CommentListCreateView, SubTaskListCreateView, TaskDetailView, TaskListCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]
