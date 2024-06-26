from rest_framework import permissions
from .models import ProjectMember


class IsAdminOfProject(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only actions without specific permission check
        if view.action in ['list', 'retrieve']:
            return True

        project_id = request.data.get('project')
        project_member_id = view.kwargs.get('pk')

        if not project_id:
            if not project_member_id:
                return False
            else:
                try:
                    project_id = ProjectMember.objects.get(id=project_member_id).project.id
                except ProjectMember.DoesNotExist:
                    return False

        return ProjectMember.objects.filter(
            project_id=project_id,
            user=request.user,
            role='Admin'
        ).exists()
