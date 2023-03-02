from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title, Review
from users import permissions
from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, pk=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = int(self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = int(self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(author=user, review=review)
