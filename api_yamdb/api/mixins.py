from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'
