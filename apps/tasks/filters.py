import django_filters

from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ('project', 'epic', 'status', 'priority', 'assignee', 'author')
