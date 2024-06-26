from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from members.models import ProjectMember
from .models import Task, Comment


class IsAdminOrAssignedForComment(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow all users to list and retrieve comments if they have the right project permissions
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            task_id = request.data.get('task')
            if not task_id:
                raise PermissionDenied("Task ID is required to add a comment.")

            try:
                task = Task.objects.get(id=task_id)
                project_member = ProjectMember.objects.get(user=request.user, project=task.project)

                if project_member.role == 'Admin' or task.assigned_to == request.user:
                    return True
                raise PermissionDenied("You do not have permission to comment on this task.")
            except (Task.DoesNotExist, ProjectMember.DoesNotExist):
                raise PermissionDenied("Invalid task or you are not a member of the project.")

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
