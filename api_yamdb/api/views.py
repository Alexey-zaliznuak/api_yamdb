from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from users import permissions
from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.CategoriesRolePermission,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
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
