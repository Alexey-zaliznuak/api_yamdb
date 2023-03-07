import os

from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import User
from .tokens import generate_user_confirm_code, get_user_jwt_token
from .serializers import UserSerializer, SignUpSerializer, MeUserSerializer
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

        if not all([email, username]):
            return Response(
                {
                    'email': '' if email else ['must be not null'],
                    'username': '' if username else ['must be not null']
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not User.objects.filter(username=username, email=email).exists():
            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
            ):
                return Response(
                    'uncorrect email/username',
                    status=status.HTTP_400_BAD_REQUEST
                )

            seriaizer = SignUpSerializer(data=request.data)
            seriaizer.is_valid(raise_exception=True)

            self.send_confirm_code(
                User.objects.create(
                    **seriaizer.validated_data,
                    confirm_code=generate_user_confirm_code()
                )
            )
            return JsonResponse(request.data)

        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email'],
        )
        if not user.confirm_code:
            user.confirm_code = generate_user_confirm_code()
            user.save()

        self.send_confirm_code(user)

        return JsonResponse(request.data)

    @action(methods=["post"], detail=False)
    def token(self, request):
        username = request.data.get('username')
        code = request.data.get('confirmation_code')

        if not all([username, code]):
            return Response(
                {'msg': [username]},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, username=username)

        code_error = self.validate_code(code)
        if code_error:
            return Response(
                {'msg': code_error},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'token': get_user_jwt_token(user)},
        )

    def send_confirm_code(self, user):
        send_mail(
            'Hi! you have made the request on APIYaMDb.',
            (
                'Hi! you have made the request on APIYaMDb.'
                f'Your confirm code: "{user.confirm_code}"'
            ),
            os.getenv("EMAIL_HOST_USER"),
            [user.email]
        )
        print('sensendsendsend')

    def validate_code(self, code):
        if not isinstance(code, str):
            return 'code must be str'
        if len(code) < 6:
            return 'invalid code len'
