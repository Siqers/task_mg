"""
Root URL configuration for the project.

This module defines the main URL routing for the Django application.
It connects different app routes and exposes API documentation endpoints.

Routes included:
- Django admin panel
- Authentication API
- Projects API
- Tasks API
- OpenAPI schema generation
- Swagger UI documentation
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.projects.urls')),
    path('api/', include('apps.tasks.urls')),
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
]