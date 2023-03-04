from django.core.exceptions import ValidationError
from rest_framework import serializers
from .validators import validate_username
from .models import User
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator],
    )
