import os

from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .tokens import generate_user_confirm_code, get_user_jwt_token
from .serializers import UserSerializer
from .validators import validate_username, validate_email

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from rest_framework.renderers import JSONRenderer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, filter_backends=(), url_path='me', name = "Get me")
    def get_me(self, request):
        self.kwargs.update(username=request.user.username)
        return self.retrieve(request, request.user.username)

    @get_me.mapping.patch
    # @action(methods=['PATCH'], detail=False, filter_backends=(), url_path='me')
    def patch_me(self, request):
        self.kwargs.update(username=request.user.username)
        return self.update(request, request.user.username)


class AUTHApiView(viewsets.ViewSet):
    permission_classes = ()

    @action(methods=["post"],detail=False)
    def signup(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        username_error = validate_username(username)
        email_error = validate_email(email)
        if email_error or username_error:
            content = {
                "erorr":"not valid data",
                'username_error': username_error,
                'email_error': email_error,
            }

            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )

        if not user.confirm_code:
            user.confirm_code = generate_user_confirm_code(user)

        send_mail(
            'Hi! you have made the request on APIYaMDb.',
            (
                'Hi! you have made the request on APIYaMDb.'
                f'Your confirm code: "{user.confirm_code}"'
            ),
            os.getenv("EMAIL_HOST_USER"),
            [email],
            fail_silently=False,
        )

        return JsonResponse({'username':username, 'email':email})

    @action(methods=["post"],detail=False)
    def token(self, request):
        username = request.data.get('username')
        code = request.data.get('confirmation_code')

        username_error = validate_username(username)
        code_error = None if isinstance(code, str) else 'code must be str'

        if code_error or username_error:
            content = {
                "erorr":"not valid data",
                'username_error': username_error,
                'email_confirm_code_error': code_error,
            }

            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username, confirm_code=code)

        return Response(
            {'token':get_user_jwt_token(user)},
        )
