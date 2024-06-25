from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):

        if any(isinstance(perm(), AllowAny) for perm in request.resolver_match.func.cls.permission_classes):
            print('$$$$$$$$$$$$$$$$')

            return None

        header = self.get_header(request)
        # print('$$$$$$$$$$$$$$$$', header)
        if header is None:
            raw_token = request.COOKIES.get('access_token')
            if raw_token is None:
                return None
        else:
            raw_token = self.get_raw_token(header)

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except Exception as e:
            raise AuthenticationFailed('Invalid token')
