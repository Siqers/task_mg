from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, permissions

from apps.tasks.filters import TaskFilter
from apps.tasks.models import Comment, SubTask, Task
from apps.tasks.permissions import IsTaskAuthorOrAssigneeOrReadOnly
from apps.tasks.serializers import CommentSerializer, SubTaskSerializer, TaskSerializer


@extend_schema_view(
    get=extend_schema(tags=['Tasks'], summary='List tasks'),
    post=extend_schema(tags=['Tasks'], summary='Create task', request=TaskSerializer, responses={201: TaskSerializer}),
)
class TaskListCreateView(generics.ListCreateAPIView):
    '''API view for listing and creating tasks.'''
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TaskFilter
    search_fields = ('title', 'description', 'project__name')
    ordering_fields = ('created_at', 'due_date', 'priority', 'status')
    ordering = ('-created_at',)

    def get_queryset(self):
        '''Optimize queryset with select_related and prefetch_related to reduce database queries.'''
        return (
            Task.objects.select_related('project', 'epic', 'author', 'assignee')
            .prefetch_related('tags', 'subtasks', 'comments__author')
        )

    def perform_create(self, serializer):
        '''Automatically set the author of the task to the current user when creating a new task.'''
        serializer.save(author=self.request.user)


@extend_schema_view(
    get=extend_schema(tags=['Tasks'], summary='Retrieve task', responses={200: TaskSerializer}),
    patch=extend_schema(tags=['Tasks'], summary='Update task', request=TaskSerializer, responses={200: TaskSerializer}),
    delete=extend_schema(tags=['Tasks'], summary='Delete task', responses={204: OpenApiResponse(description='Deleted successfully')}),
)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    ''''API view for retrieving, updating, and deleting a specific task.'''
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskAuthorOrAssigneeOrReadOnly]

    def get_queryset(self):
        '''Optimize queryset with select_related and prefetch_related to reduce database queries.'''
        return (
            Task.objects.select_related('project', 'epic', 'author', 'assignee')
            .prefetch_related('tags', 'subtasks', 'comments__author')
        )


@extend_schema_view(
    get=extend_schema(tags=['SubTasks'], summary='List subtasks'),
    post=extend_schema(tags=['SubTasks'], summary='Create subtask', request=SubTaskSerializer, responses={201: SubTaskSerializer}),
)
class SubTaskListCreateView(generics.ListCreateAPIView):
    ''''API view for listing and creating subtasks.'''
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubTask.objects.select_related('task', 'task__project')
    search_fields = ('title', 'task__title')
    ordering_fields = ('id', 'task')
    ordering = ('id',)


@extend_schema_view(
    get=extend_schema(tags=['Comments'], summary='List comments'),
    post=extend_schema(tags=['Comments'], summary='Create comment', request=CommentSerializer, responses={201: CommentSerializer}),
)
class CommentListCreateView(generics.ListCreateAPIView):
    '''API view for listing and creating comments.'''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.select_related('task', 'author', 'task__project')
    search_fields = ('body', 'author__email', 'task__title')
    ordering_fields = ('created_at',)
    ordering = ('-created_at',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
