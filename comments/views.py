from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from .filters import CommentFilter
from .models import Comment, Task
from .serializers import CommentSerializer
from .permissions import IsAdminOrAssignedForComment
from members.models import ProjectMember
from django.db.models import Q


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedForComment]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        project_memberships = ProjectMember.objects.filter(user=user)

        admin_project_ids = project_memberships.filter(role='Admin').values_list('project_id', flat=True)

        assigned_task_ids = Task.objects.filter(assigned_to=user).values_list('id', flat=True)

        return Comment.objects.filter(Q(task__project_id__in=admin_project_ids) | Q(task__id__in=assigned_task_ids))
