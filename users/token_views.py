from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_data = serializer.validated_data
        response = Response(response_data, status=status.HTTP_200_OK)

        # Check if setCookie is true in the request body
        if request.data.get('setCookie', False):
            response.set_cookie(
                key='access_token',
                value=str(response_data['access']),
                httponly=True,
                secure=True,  # Ensure this is only sent over HTTPS
                samesite='Lax',
            )
            response.set_cookie(
                key='refresh_token',
                value=str(response_data['refresh']),
                httponly=True,
                secure=True,
                samesite='Lax',
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_data = serializer.validated_data
        response = Response(response_data, status=status.HTTP_200_OK)

        # Check if setCookie is true in the request body
        if request.data.get('setCookie', False):
            response.set_cookie(
                key='access_token',
                value=str(response_data['access']),
                httponly=True,
                secure=True,  # Ensure this is only sent over HTTPS
                samesite='Lax',
            )

        return response
