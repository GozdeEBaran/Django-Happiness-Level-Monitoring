from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


def get_user_is_authorized(request):
    # validate the token if token is sent
    # otherwise return False
    auth_class = JWTAuthentication()
    res = auth_class.authenticate(request)
    if res is None:
        return False

    return True


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
