from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ready_page

urlpatterns = [
    path('', views.index, name='index'),
    path('ready_page/', ready_page, name='ready_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)