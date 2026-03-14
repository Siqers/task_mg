from django.urls import path

from apps.projects.views import EpicListCreateView, ProjectDetailView, ProjectListCreateView, SprintListCreateView
'''URL patterns for the projects app.'''
urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('sprints/', SprintListCreateView.as_view(), name='sprint-list-create'),
    path('epics/', EpicListCreateView.as_view(), name='epic-list-create'),
]
