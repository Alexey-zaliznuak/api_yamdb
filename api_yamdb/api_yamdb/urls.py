from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('schema-swagger-ui')), name='index')
]
