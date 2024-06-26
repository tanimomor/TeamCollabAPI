from rest_framework import serializers

from projects.models import Project
from .models import ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']

    def validate(self, data):
        project = data.get('project')
        user = data.get('user')

        # Check if the user is already a member of the project
        if ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError("This user is already a member of the project.")

        return data
