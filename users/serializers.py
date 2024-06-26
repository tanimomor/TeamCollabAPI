# users/serializers.py
from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    username = serializers.CharField(
        min_length=4,
        max_length=150,
        error_messages={
            'min_length': 'Username must be at least 4 characters long.',
            'max_length': 'Username cannot exceed 150 characters.'
        }
    )

    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[
            RegexValidator(
                regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message=(
                    'Password must contain at least one uppercase letter, '
                    'one lowercase letter, one number, and one special character.'
                )
            )
        ],
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )

    def validate(self, data):
        if not data.get('first_name') and not data.get('last_name'):
            raise serializers.ValidationError(
                'At least one of first_name or last_name must be provided.'
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
