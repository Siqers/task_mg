from django.db.models import Count
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, permissions

from apps.projects.filters import EpicFilter, SprintFilter
from apps.projects.models import Epic, Membership, Project, Sprint
from apps.projects.permissions import IsProjectOwner
from apps.projects.serializers import EpicSerializer, ProjectSerializer, SprintSerializer


@extend_schema_view(
    get=extend_schema(tags=['Projects'], summary='List projects'),
    post=extend_schema(tags=['Projects'], summary='Create project', request=ProjectSerializer, responses={201: ProjectSerializer}),
)
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('name', 'description', 'owner__email', 'owner__full_name')
    ordering_fields = ('created_at', 'name')
    ordering = ('-created_at',)

    def get_queryset(self):
        return Project.objects.select_related('owner').annotate(members_count=Count('memberships', distinct=True))

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        Membership.objects.get_or_create(
            user=self.request.user,
            project=project,
            defaults={'role': Membership.ROLE_CAPTAIN},
        )


@extend_schema_view(
    get=extend_schema(tags=['Projects'], summary='Retrieve project', responses={200: ProjectSerializer}),
    patch=extend_schema(tags=['Projects'], summary='Update project', request=ProjectSerializer, responses={200: ProjectSerializer}),
    delete=extend_schema(tags=['Projects'], summary='Delete project', responses={204: OpenApiResponse(description='Deleted successfully')}),
)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        return Project.objects.select_related('owner').annotate(members_count=Count('memberships', distinct=True))


@extend_schema_view(
    get=extend_schema(tags=['Sprints'], summary='List sprints'),
    post=extend_schema(tags=['Sprints'], summary='Create sprint', request=SprintSerializer, responses={201: SprintSerializer}),
)
class SprintListCreateView(generics.ListCreateAPIView):
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sprint.objects.select_related('project')
    filterset_class = SprintFilter
    search_fields = ('title', 'project__name')
    ordering_fields = ('start_date', 'end_date', 'title')
    ordering = ('-start_date',)


@extend_schema_view(
    get=extend_schema(tags=['Epics'], summary='List epics'),
    post=extend_schema(tags=['Epics'], summary='Create epic', request=EpicSerializer, responses={201: EpicSerializer}),
)
class EpicListCreateView(generics.ListCreateAPIView):
    serializer_class = EpicSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Epic.objects.select_related('project', 'sprint')
    filterset_class = EpicFilter
    search_fields = ('title', 'description', 'project__name')
    ordering_fields = ('id', 'title', 'status')
    ordering = ('id',)
