from django.conf import settings
from django.conf.urls.static import static
# from django.urls import path
#
# from rest_framework.routers import DefaultRouter
# from tobaccos.views import TobaccoViewSet, TobaccoCreateView
#
# router = DefaultRouter()
# router.register('api/v1/tobaccos', TobaccoViewSet)
#
# urlpatterns = [
#                   path('api/v1/tobaccos/create/', TobaccoCreateView.as_view(), name='tobaccos-create')
#               ] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path

from tobaccos.views import (
    TobaccoListAPIView,
    TobaccoDetailAPIView,
    TobaccoCreateAPIView,
    TobaccoUpdateAPIView,
    TobaccoPartialUpdateAPIView,
    TobaccoDestroyAPIView,
)

urlpatterns = [
    path('api/v1/tobaccos/list/', TobaccoListAPIView.as_view(), name='tobaccos-list'),
    path('api/v1/tobaccos/detail/', TobaccoDetailAPIView.as_view(), name='tobaccos-detail'),
    path('api/v1/tobaccos/create/', TobaccoCreateAPIView.as_view(), name='tobaccos-create'),
    path('api/v1/tobaccos/update/<uuid:pk>/', TobaccoUpdateAPIView.as_view(), name='tobaccos-update'),
    path('api/v1/tobaccos/partial-update/<uuid:pk>/', TobaccoPartialUpdateAPIView.as_view(), name='tobaccos-partial-update'),
    path('api/v1/tobaccos/delete/<uuid:pk>/', TobaccoDestroyAPIView.as_view(), name='tobaccos-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)