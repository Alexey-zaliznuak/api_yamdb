from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS

from reviews.models import Category, Genre, Title, Review
from users import permissions
from users.permissions import TitlesRolePermission
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.CategoriesRolePermission,)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.GenresRolePermission,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (TitlesRolePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.title_id
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.title_id
        title = get_object_or_404(Title, pk=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (permissions.ReviewsRolePermission(),)

    @property
    def title_id(self) -> int:
        return int(self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.review_id
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (permissions.CommentsRolePermission(),)

    def perform_create(self, serializer):
        review_id = self.review_id
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(author=user, review=review)

    @property
    def review_id(self) -> int:
        return int(self.kwargs.get('review_id'))
