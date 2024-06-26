from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from .filters import ProjectMemberFilter
from .models import ProjectMember
from .permissions import IsAdminOfProject
from .serializers import ProjectMemberSerializer


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOfProject]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectMemberFilter
