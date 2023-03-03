from django.core.exceptions import ValidationError
from rest_framework import serializers
from .validators import validate_username
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
