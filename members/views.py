from rest_framework import viewsets, permissions
from .models import ProjectMember
from .serializers import ProjectMemberSerializer

class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
