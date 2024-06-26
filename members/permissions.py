from rest_framework import permissions
from .models import ProjectMember


class IsAdminOfProject(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only actions without specific permission check
        if view.action in ['list', 'retrieve']:
            return True

        project_id = request.data.get('project')
        print(project_id)
        if not project_id:
            return False

        return ProjectMember.objects.filter(
            project_id=project_id,
            user=request.user,
            role='Admin'
        ).exists()
