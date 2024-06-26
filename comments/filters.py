import django_filters
from .models import Comment


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'content': ['icontains'],
            'user': ['exact'],
            'task': ['exact'],
            'created_at': ['exact', 'year__gt', 'year__lt'],
        }
