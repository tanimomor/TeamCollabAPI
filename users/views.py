from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Define different permissions for different actions
        print('action', self.action)
        if self.action == 'register' or self.action == 'login':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response_data = {
            'message': 'User registered successfully',
            'refresh': str(refresh),
            'access': str(access),
            'user': serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        serializer = self.get_serializer(user)
        response_data = {
            'message': 'Login successful',
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(access),
        }
        return Response(response_data, status=status.HTTP_200_OK)



class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        print('Test')
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
