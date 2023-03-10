import os

from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .tokens import generate_user_confirm_code, get_user_jwt_token
from .serializers import (
    SignUpSerializer,
    GetTokenSerializer,
    UserSerializer,
)
from .permissions import IsAdminUserOrRoleAdmin

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUserOrRoleAdmin)
    filter_backends = (filters.SearchFilter, )
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', "patch", 'delete']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        filter_backends=(),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        self.kwargs.update(username=request.user.username)
        if request.method == 'PATCH':
            return self.partial_update(request, request.user.username)

        return self.retrieve(request, request.user.username)


class AUTHApiView(viewsets.ViewSet):
    permission_classes = ()

    @action(methods=["post"], detail=False)
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.send_confirm_code(
            User.objects.get_or_create(
                **serializer.validated_data,
            )[0]
        )
        return JsonResponse(request.data)

    @action(methods=["post"], detail=False)
    def token(self, request):
        seriaizer = GetTokenSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)

        user = get_object_or_404(User, **seriaizer.validated_data)

        return Response(
            {'token': get_user_jwt_token(user)},
        )

    def send_confirm_code(self, user):
        code = user.confirmation_code
        if not code:
            user.confirmation_code = code = generate_user_confirm_code()

        send_mail(
            'Hi! you have made the request on APIYaMDb.',
            (
                'Hi! you have made the request on APIYaMDb.'
                f'Your confirm code: "{code}"'
            ),
            os.getenv("EMAIL_HOST_USER"),
            [user.email]
        )
