from rest_framework_simplejwt.tokens import RefreshToken
from hashlib import sha512


def generate_user_confirm_code(user) -> str:
    data:str = user.username + user.password + user.email

    return sha512(data.encode('utf-8')).hexdigest()

def get_user_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
