import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['exact', 'icontains'],
            'status': ['exact'],
            'priority': ['exact'],
            'assigned_to': ['exact'],
            'project': ['exact'],
            'due_date': ['exact', 'year__gt', 'year__lt'],
        }
