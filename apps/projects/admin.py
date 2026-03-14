from django.contrib import admin

from apps.projects.models import Epic, Membership, Project, Sprint


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'description', 'owner__email', 'owner__full_name')
    list_filter = ('created_at',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')
    search_fields = ('user__email', 'user__full_name', 'project__name')
    list_filter = ('role', 'joined_at')


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'is_active')
    search_fields = ('title', 'project__name')
    list_filter = ('is_active', 'start_date', 'end_date')


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status')
    search_fields = ('title', 'description', 'project__name')
    list_filter = ('status', 'project')
