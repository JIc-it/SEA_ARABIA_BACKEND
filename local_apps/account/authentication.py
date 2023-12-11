
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            print("Authenticating request:", request)  # Debug print
            # Rest of your authentication logic
            user = super().authenticate(request)

            if user is not None and isinstance(user[0], Token):
                token = user[0]
                token['user_id'] = user[1].id if user[1] else None
                print("Token user ID:", token['user_id'])  # Debug print

            return user

        except AuthenticationFailed as e:
            print("Authentication failed:", str(e))  # Debug print
            raise AuthenticationFailed('Custom error message: Authentication failed.')

        return None
