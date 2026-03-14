from django.urls import path

from apps.users.views import LoginView, ProfileView, RefreshTokenView, RegisterView

'''
URL patterns for user-related endpoints, including registration, login, token refresh, and profile management.'''

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
