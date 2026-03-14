from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CAPTAIN = 'captain'
    ROLE_MEMBER = 'member'
    ROLE_VIEWER = 'viewer'

    ROLE_CHOICES = (
        (ROLE_CAPTAIN, 'Captain'),
        (ROLE_MEMBER, 'Member'),
        (ROLE_VIEWER, 'Viewer'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        ordering = ['project_id', 'user_id']

    def __str__(self):
        return f'{self.user.email} - {self.project.name} ({self.role})'


class Sprint(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='sprints')
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['project_id', '-start_date']

    def __str__(self):
        return self.title


class Epic(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_CLOSED, 'Closed'),
    )

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='epics')
    sprint = models.ForeignKey('projects.Sprint', on_delete=models.SET_NULL, related_name='epics', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    class Meta:
        ordering = ['project_id', 'id']

    def __str__(self):
        return self.title
