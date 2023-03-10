from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from django.shortcuts import get_object_or_404


MIN_CODE_LEN = 6


class UserSerializer(serializers.ModelSerializer):
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

    def update(self, user, validated_data):
        for key, value in validated_data.items():
            if (
                key == 'role'
                and not user.has_admin_permissions
            ):
                value = user.role

            user.__setattr__(key, value)

        user.save()
        return user


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

    def validate(self, data):
        username = data['username']
        email = data['email']

        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(Q(username=username) | Q(email=email)):
                raise ValidationError('uncorrect email/username')

        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()

    def validate(sef, data):
        username = data['username']
        code = data['confirmation_code']

        UnicodeUsernameValidator()(username)
        get_object_or_404(User, username=username)

        if len(code) < MIN_CODE_LEN:
            raise ValidationError('invalid code')

        return data
