from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_REVIEW = 'review'
    STATUS_DONE = 'done'

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CRITICAL = 'critical'

    STATUS_CHOICES = (
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_REVIEW, 'Review'),
        (STATUS_DONE, 'Done'),
    )
    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_CRITICAL, 'Critical'),
    )

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    epic = models.ForeignKey('projects.Epic', on_delete=models.SET_NULL, related_name='tasks', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_tasks')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='assigned_tasks', blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField('tasks.Tag', related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['task_id', 'id']

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.email} on {self.task.title}'
