from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.tasks.models import Comment, SubTask, Tag, Task

User = get_user_model()


class TaskUserMiniSerializer(serializers.ModelSerializer):
    '''Serializer for representing users in a minimal format (id, email, full_name)'''
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')


class TagSerializer(serializers.ModelSerializer):
    '''Serializer for representing tags (id, name)'''
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class SubTaskSerializer(serializers.ModelSerializer):
    '''Serializer for representing subtasks (id, task, title, is_completed)'''
    class Meta:
        model = SubTask
        fields = ('id', 'task', 'title', 'is_completed')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for representing comments (id, task, author, body, created_at)'''
    author = TaskUserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'task', 'author', 'body', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')


class TaskSerializer(serializers.ModelSerializer):
    '''Serializer for representing tasks with all details, including related fields'''
    author = TaskUserMiniSerializer(read_only=True)
    assignee = TaskUserMiniSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, required=False, source='tags'
    )
    subtasks = SubTaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'epic',
            'title',
            'description',
            'status',
            'priority',
            'author',
            'assignee',
            'assignee_id',
            'due_date',
            'tags',
            'tag_ids',
            'subtasks',
            'comments',
            'created_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'assignee', 'tags', 'subtasks', 'comments')
