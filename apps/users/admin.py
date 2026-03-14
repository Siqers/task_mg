from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''Admin interface for the custom User model.'''
    list_display = ('email', 'full_name', 'is_staff')
    search_fields = ('email', 'full_name', 'phone')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'created_at')
    ordering = ('email',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'full_name', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
            },
        ),
    )
