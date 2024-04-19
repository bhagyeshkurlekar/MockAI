from rest_framework.authtoken.models import Token
from rest_framework import status


def user_detail(user):
    try:
        token = user.auth_token.key
    except:
        token = Token.objects.create(user=user)
        token = token.key
    user_json = {
        "id": user.id,
        "token": token,
        "status": status.HTTP_200_OK
    }
    return user_json