from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

from .views import TitleViewSet, GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('users.urls')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="YaMDb API",
      default_version='v1',
      description="Документация для API YaMDb",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="zaliznuak50@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]
