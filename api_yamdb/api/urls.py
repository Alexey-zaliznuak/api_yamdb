from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genre', GenreViewSet, basename='genre')
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/', include(router.urls)),
]
