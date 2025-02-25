from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls import handler404
from main.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="inHookah API",
        default_version='v1',
        description="API documentation",
    ),
    public=False,  # Не делаем документацию публичной
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(SessionAuthentication, BasicAuthentication)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('bowls.urls')),  # Добавляем маршруты из bowls
    path('', include('manufacturers.urls')),  # Добавляем маршруты из manufacturers
    path('', include('tobaccos.urls')),  # Добавляем маршруты из tobaccos
    path('', include('mixes.urls')),  # Добавляем маршруты из mixes
    path('', include('users.urls')),  # Добавляем маршруты из users
    path('', include('tastecategories.urls')),  # Добавляем маршруты из users
]
