from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.projects.models import Epic, Membership, Project, Sprint

User = get_user_model()


class OwnerMiniSerializer(serializers.ModelSerializer):
    '''Serializer for representing project owners with minimal information.'''
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')


class MembershipSerializer(serializers.ModelSerializer):
    '''Serializer for representing project memberships, including user details.'''
    user = OwnerMiniSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'user', 'role', 'joined_at')


class ProjectSerializer(serializers.ModelSerializer):
    '''Serializer for representing projects, including owner details and member count.'''
    owner = OwnerMiniSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'members_count', 'created_at')
        read_only_fields = ('id', 'owner', 'members_count', 'created_at')


class SprintSerializer(serializers.ModelSerializer):
    '''Serializer for representing sprints, including project details.'''
    class Meta:
        model = Sprint
        fields = ('id', 'project', 'title', 'start_date', 'end_date', 'is_active')
        read_only_fields = ('id',)


class EpicSerializer(serializers.ModelSerializer):
    '''Serializer for representing epics, including project and sprint details.'''
    class Meta:
        model = Epic
        fields = ('id', 'project', 'sprint', 'title', 'description', 'status')
        read_only_fields = ('id',)
