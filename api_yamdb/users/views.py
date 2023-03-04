import os

from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .tokens import generate_user_confirm_code, get_user_jwt_token
from .serializers import UserSerializer, SignUpSerializer
from .validators import validate_username, validate_email, validate_code

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
    # permission_classes = (IsAuthenticated, IsAdminUser)
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
        seriaizer = SignUpSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)

        user, created = User.objects.get_or_create(
            **seriaizer.validated_data,
            confirm_code = generate_user_confirm_code()
        )

        print(created)

        send_mail(
            'Hi! you have made the request on APIYaMDb.',
            (
                'Hi! you have made the request on APIYaMDb.'
                f'Your confirm code: "{user.confirm_code}"'
            ),
            os.getenv("EMAIL_HOST_USER"),
            [user.email],
            fail_silently=False,
        )

        return JsonResponse(request.data)

    @action(methods=["post"],detail=False)
    def token(self, request):
        username = request.data.get('username')
        code = request.data.get('confirmation_code')

        if not all([username, code]):
            return Response(
                {'msg': [username]},
                status=status.HTTP_400_BAD_REQUEST
            )

        print(User.objects.all())      
        user = get_object_or_404(User, username=username)

        code_error = validate_code(code)
        if code_error:
            return Response(
                {'msg': code_error},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'token':get_user_jwt_token(user.first())},
        )
