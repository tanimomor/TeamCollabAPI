from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response

from teamcollab.permissions import IsOwnerOrReadOnly
from .models import ProjectMember
from .permissions import IsAdminOfProject
from .serializers import ProjectMemberSerializer


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOfProject]
