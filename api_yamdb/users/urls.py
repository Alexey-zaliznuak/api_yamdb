from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    AUTHApiView,
    UserViewSet,
)

router = DefaultRouter()
router.register('auth', AUTHApiView, basename="auth")
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
