from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator


def validate_username(username):
    if not username:
        return "username must be not null"
    if username == 'me':
        return 'uncorrect username'
    try:
        RegexValidator(r"^[\w.@+-]+\Z")(username)
        MaxLengthValidator(150)(username)
    except ValidationError as e:
        return e.message

def validate_email(email):
    if not email:
        return "email must be not null"
    try:
        MaxLengthValidator(254)(email)
    except ValidationError as e:
        return e.message

def validate_code(code):
    if not isinstance(code, str):
        return 'code must be str'
    if len(code) < 6:
        return 'invalid code len'
