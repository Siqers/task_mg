import django_filters

from apps.projects.models import Epic, Sprint


class SprintFilter(django_filters.FilterSet):
    class Meta:
        model = Sprint
        fields = ('project', 'is_active')


class EpicFilter(django_filters.FilterSet):
    class Meta:
        model = Epic
        fields = ('project', 'sprint', 'status')
