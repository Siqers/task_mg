import django_filters

from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    '''Фильтр для задач, позволяющий фильтровать по проекту, эпикам, статусу, приоритету, исполнителю и автору.'''
    class Meta:
        model = Task
        fields = ('project', 'epic', 'status', 'priority', 'assignee', 'author')
