from rest_framework import serializers
from .models import Task
from datetime import datetime

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']

    title = serializers.CharField(
        max_length=100,
        error_messages={
            'required': 'Title is required.',
            'blank': 'Title cannot be empty.',
            'max_length': 'Title cannot exceed 100 characters.'
        }
    )

    status = serializers.ChoiceField(
        choices=['To Do', 'In Progress', 'Done'],
        error_messages={
            'required': 'Status is required.',
            'blank': 'Status cannot be empty.',
            'invalid_choice': 'Invalid status. Must be one of: To Do, In Progress, Done.'
        }
    )

    priority = serializers.ChoiceField(
        choices=['Low', 'Medium', 'High'],
        error_messages={
            'required': 'Priority is required.',
            'blank': 'Priority cannot be empty.',
            'invalid_choice': 'Invalid priority. Must be one of: Low, Medium, High.'
        }
    )

    due_date = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'],
        error_messages={
            'required': 'Due date is required.',
            'blank': 'Due date cannot be empty.',
            'invalid': 'Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ.'
        }
    )
