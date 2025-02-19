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

from mixes.views import *

urlpatterns = [
    path('api/v1/mixes/', MixesListView.as_view(), name='mixes-list-post'),
    path('api/v1/mixes/<uuid:mix_id>/', MixDetailView.as_view(), name='mix-detail'),
    path('api/v1/mixes/<uuid:mix_id>/likes/', MixLikeAPIView.as_view(), name='mix_like'),
    path('api/v1/mixes/<uuid:mix_id>/favorites/', MixFavoriteAPIView.as_view(), name='mix_favorite'),

    # Создание объектов через отдельные эндпоинты /create/
    path('api/v1/mixes/create/', MixCreateView.as_view(), name='mixes-create')
]
