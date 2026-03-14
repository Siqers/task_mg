from django.db.models import Count

from django.core.cache import cache

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
    """
    View for listing and creating projects.
    Uses Redis cache for optimizing project list retrieval.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ('name', 'description', 'owner__email', 'owner__full_name')
    ordering_fields = ('created_at', 'name')
    ordering = ('-created_at',)

    def get_queryset(self):
        """
        Return projects where the user is a member or owner,
        annotated with members count.
        Cached in Redis for performance improvement.
        """
        cache_key = f"projects_user_{self.request.user.id}"
        projects = cache.get(cache_key)

        if projects is None:
            projects = (
                Project.objects
                .select_related('owner')
                .annotate(members_count=Count('memberships', distinct=True))
            )
            cache.set(cache_key, projects, 300)  # cache for 5 minutes

        return projects

    def perform_create(self, serializer):
        """
        Create a new project and add creator as captain.
        Clears related Redis cache after creation.
        """
        project = serializer.save(owner=self.request.user)

        Membership.objects.get_or_create(
            user=self.request.user,
            project=project,
            defaults={'role': Membership.ROLE_CAPTAIN},
        )

        # Invalidate cache after creating project
        cache.delete(f"projects_user_{self.request.user.id}")


@extend_schema_view(
    get=extend_schema(tags=['Projects'], summary='Retrieve project', responses={200: ProjectSerializer}),
    patch=extend_schema(tags=['Projects'], summary='Update project', request=ProjectSerializer, responses={200: ProjectSerializer}),
    delete=extend_schema(tags=['Projects'], summary='Delete project', responses={204: OpenApiResponse(description='Deleted successfully')}),
)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a project.
    Only the owner can update or delete.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        return (
            Project.objects
            .select_related('owner')
            .annotate(members_count=Count('memberships', distinct=True))
        )

    def perform_update(self, serializer):
        """
        Update project and invalidate cache.
        """
        instance = serializer.save()
        cache.delete(f"projects_user_{self.request.user.id}")
        return instance

    def perform_destroy(self, instance):
        """
        Delete project and invalidate cache.
        """
        cache.delete(f"projects_user_{self.request.user.id}")
        instance.delete()


@extend_schema_view(
    get=extend_schema(tags=['Sprints'], summary='List sprints'),
    post=extend_schema(tags=['Sprints'], summary='Create sprint', request=SprintSerializer, responses={201: SprintSerializer}),
)
class SprintListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating sprints.
    Cached using Redis.
    """
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sprint.objects.select_related('project')

    filterset_class = SprintFilter
    search_fields = ('title', 'project__name')
    ordering_fields = ('start_date', 'end_date', 'title')
    ordering = ('-start_date',)

    def list(self, request, *args, **kwargs):
        cache_key = "sprints_list"
        data = cache.get(cache_key)

        if data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, 300)
            return response

        return Response(data)

def Response(data):
    raise NotImplementedError


@extend_schema_view(
    get=extend_schema(tags=['Epics'], summary='List epics'),
    post=extend_schema(tags=['Epics'], summary='Create epic', request=EpicSerializer, responses={201: EpicSerializer}),
)
class EpicListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating epics.
    Cached using Redis.
    """
    serializer_class = EpicSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Epic.objects.select_related('project', 'sprint')

    filterset_class = EpicFilter
    search_fields = ('title', 'description', 'project__name')
    ordering_fields = ('id', 'title', 'status')
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        cache_key = "epics_list"
        data = cache.get(cache_key)

        if data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, 300)
            return response

        return Response(data)