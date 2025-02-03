"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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


# Кастомный обработчик 404
def custom_404_view(request, exception=None):
    return JsonResponse({
        "status": "bad",
        "code": 404,
        "message": "Ресурс не найден",
        "data": None
    }, status=404)


# Кастомный обработчик 500
def custom_500_view(request):
    return JsonResponse({
        "status": "bad",
        "code": 500,
        "message": "Внутренняя ошибка сервера",
        "data": None
    }, status=500)


handler404 = custom_404_view
handler500 = custom_500_view

schema_view = get_schema_view(
    openapi.Info(
        title="inHookah API",
        default_version='v1',
        description="API documentation for the Tobacco Mix Management System",
    ),
    public=False,  # Не делаем документацию публичной
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(SessionAuthentication, BasicAuthentication),
)

router = DefaultRouter()
router.register('api/v1/tobaccos', TobaccoViewSet)
# router.register('api/v1/mixes', MixesViewSet)
router.register('api/v1/manufacturers', ManufacturersViewSet)
router.register('api/v1/bowls', BowlsViewSet)
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  # Djoser создаст набор необходимых элементов
                  # Базовые, для управления пользователями в Django:
                  path('api/v1/auth/', include('djoser.urls')),
                  path('api/v1/my_profile/', UserProfileView.as_view(), name='user-profile'),
                  # JWT-эндпоинты, для управления JWT-токенами:
                  path('api/v1/', include('djoser.urls.jwt')),
                  path('api/v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/v1/mixes/', MixesListView.as_view(), name='mixes-list-post'),
                  path('api/v1/mixes/<uuid:mix_id>/', MixDetailView.as_view(), name='mix-detail'),
                  path('api/v1/mixes/<uuid:mix_id>/likes/', MixLikeAPIView.as_view(), name='mix_like'),
                  path('api/v1/mixes/<uuid:mix_id>/favorites/', MixFavoriteAPIView.as_view(), name='mix_favorite'),

                  # Создание объектов через отдельные эндпоинты /create/
                  path('api/v1/mixes/create/', MixCreateView.as_view(), name='mixes-create'),
                  path('api/v1/tobaccos/create/', TobaccoCreateView.as_view(), name='tobaccos-create'),
                  path('api/v1/manufacturers/create/', ManufacturerCreateView.as_view(), name='manufacturers-create'),
                  path('api/v1/bowls/create/', BowlCreateView.as_view(), name='bowls-create'),
                  path('api/v1/taste-categories/create/', TasteCategoryCreateView.as_view(),
                       name='taste-categories-create'),

              ] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
