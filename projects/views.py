from rest_framework import viewsets, permissions

from members.models import ProjectMember
from .models import Project
from .serializers import ProjectSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProjectFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user=self.request.user, role='Admin')
