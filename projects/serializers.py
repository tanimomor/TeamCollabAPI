from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']
