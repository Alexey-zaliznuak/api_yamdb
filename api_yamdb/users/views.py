import os

from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .tokens import generate_user_confirm_code, get_user_jwt_token
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    MeUserSerializer,
    GetTokenSerializer,    
)
from .permissions import IsAdminUserOrRoleAdmin

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
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
        serializer_class=MeUserSerializer,
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
        username = request.data.get('username')
        email = request.data.get('email')

        seriaizer = SignUpSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)
        print('abobaabobaaboba')
        if not User.objects.filter(username=username, email=email).exists():
            print("wwwwwwwwwtttttttttfffffff")
            self.send_confirm_code(
                User.objects.create(
                    **seriaizer.validated_data,
                    confirmation_code=generate_user_confirm_code()
                )
            )
            return JsonResponse(request.data)

        user =  get_object_or_404(User, **seriaizer.validated_data)
        self.send_confirm_code(user)

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
        send_mail(
            'Hi! you have made the request on APIYaMDb.',
            (
                'Hi! you have made the request on APIYaMDb.'
                f'Your confirm code: "{user.confirmation_code}"'
            ),
            os.getenv("EMAIL_HOST_USER"),
            [user.email]
        )
