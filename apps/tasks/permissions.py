from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTaskAuthorOrAssigneeOrReadOnly(BasePermission):
    '''Only the task author or assignee can modify this task.'''
    message = 'Only the task author or assignee can modify this task.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or obj.assignee == request.user


class IsCommentAuthorOrReadOnly(BasePermission):
    '''Only the comment author can delete or modify this comment.'''
    message = 'Only the comment author can delete or modify this comment.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
