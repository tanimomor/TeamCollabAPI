from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from members.models import ProjectMember


class IsAdminForProject(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            project_id = request.data.get('project') if request.method == 'POST' else view.get_object().project_id
            try:
                project_member = ProjectMember.objects.get(user=request.user, project_id=project_id)
                if project_member.role != 'Admin':
                    raise PermissionDenied("You do not have permission to add or delete tasks in this project.")

                # Check if the assigned_to user is a member of the project (only for POST requests)
                if request.method == 'POST':
                    assigned_to_user_id = request.data.get('assigned_to')
                    if assigned_to_user_id:
                        is_member = ProjectMember.objects.filter(project_id=project_id,
                                                                 user_id=assigned_to_user_id).exists()
                        if not is_member:
                            raise ValidationError("The assigned user must be a member of the project.")

                return True
            except ProjectMember.DoesNotExist:
                raise PermissionDenied("You are not a member of this project.")
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            project_member = ProjectMember.objects.get(user=user, project=obj.project)
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == 'PUT' or request.method == 'PATCH':
                if project_member.role == 'Admin':
                    return True
                if project_member.role == 'Member' and 'status' in request.data and all(
                        field not in request.data for field in
                        ['title', 'description', 'priority', 'assigned_to', 'project', 'due_date']):
                    return True
                raise ValidationError("Members can only change the status of tasks.")

            if request.method == 'DELETE':
                if project_member.role == 'Admin':
                    return True
                raise PermissionDenied("You do not have permission to delete this task.")
        except ProjectMember.DoesNotExist:
            raise PermissionDenied("You are not a member of this project.")
