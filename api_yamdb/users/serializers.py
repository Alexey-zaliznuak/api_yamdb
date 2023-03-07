from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
        read_only_fields = ('role', )


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
    )

    def validate_username(sef, value):
        UnicodeUsernameValidator()(value)

        if value == 'me':
            raise ValidationError('uncorrect username')

        return value
