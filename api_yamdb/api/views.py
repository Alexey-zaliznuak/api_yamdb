from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from reviews.models import Category, Genre, Title
from .permissions import IsAuthorOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    # permission_classes = (IsAuthorOrReadOnly, IsAuthenticated, IsAuthenticatedOrReadOnly)
    search_fields = ('name',)
    lookup_field = ('slug',)

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

