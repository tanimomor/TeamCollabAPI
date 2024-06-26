from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']

    def validate_content(self, value):
        """
        Validate that the content field is not empty and does not exceed 1000 characters.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        max_length = 1000
        if len(value) > max_length:
            raise serializers.ValidationError(f"Content cannot exceed {max_length} characters.")
        return value
