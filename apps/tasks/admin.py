from django.contrib import admin

from apps.tasks.models import Comment, SubTask, Tag, Task


class SubTaskInline(admin.TabularInline):
    '''
    Inline admin interface for SubTask model.
    
    This allows SubTasks to be edited directly within the Task admin page.'''
    model = SubTask
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin interface for Tag model.'''
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    '''Admin interface for Task model.'''
    list_display = ('title', 'status', 'priority', 'assignee')
    search_fields = ('title', 'description', 'project__name', 'author__email', 'assignee__email')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date')
    inlines = [SubTaskInline]
    filter_horizontal = ('tags',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    '''Admin interface for SubTask model.'''
    list_display = ('title', 'task', 'is_completed')
    search_fields = ('title', 'task__title')
    list_filter = ('is_completed',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin interface for Comment model.'''
    list_display = ('author', 'task')
    search_fields = ('author__email', 'author__full_name', 'task__title', 'body')
    list_filter = ('created_at',)
