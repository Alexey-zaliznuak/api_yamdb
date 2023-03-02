from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from users import permissions
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.CategoriesRolePermission,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.GenresRolePermission,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.TitlesRolePermission,)
    pagination_class = PageNumberPagination
