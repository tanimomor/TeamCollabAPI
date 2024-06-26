from rest_framework import viewsets, permissions

from members.models import ProjectMember
from .models import Task
from .permissions import IsAdminForProject
from .serializers import TaskSerializer
from django.db.models import Q


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminForProject]

    def get_queryset(self):
        user = self.request.user

        project_memberships = ProjectMember.objects.filter(user=user)
        admin_project_ids = project_memberships.filter(role='Admin').values_list('project_id', flat=True)
        member_project_ids = project_memberships.filter(role='Member').values_list('project_id', flat=True)

        return Task.objects.filter(
            Q(project_id__in=admin_project_ids) |
            Q(project_id__in=member_project_ids, assigned_to=user)
        )



