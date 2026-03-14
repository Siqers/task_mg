from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.projects.models import Epic, Membership, Project, Sprint

User = get_user_model()


class OwnerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')


class MembershipSerializer(serializers.ModelSerializer):
    user = OwnerMiniSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ('id', 'user', 'role', 'joined_at')


class ProjectSerializer(serializers.ModelSerializer):
    owner = OwnerMiniSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'members_count', 'created_at')
        read_only_fields = ('id', 'owner', 'members_count', 'created_at')


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id', 'project', 'title', 'start_date', 'end_date', 'is_active')
        read_only_fields = ('id',)


class EpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epic
        fields = ('id', 'project', 'sprint', 'title', 'description', 'status')
        read_only_fields = ('id',)
