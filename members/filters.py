import django_filters
from .models import ProjectMember


class ProjectMemberFilter(django_filters.FilterSet):
    class Meta:
        model = ProjectMember
        fields = {
            'project': ['exact'],
            'user': ['exact'],
            'role': ['exact'],
        }
