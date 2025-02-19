from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from rest_framework.routers import DefaultRouter
from tobaccos.views import TobaccoViewSet, TobaccoCreateView

router = DefaultRouter()
router.register('api/v1/tobaccos', TobaccoViewSet)

urlpatterns = [
                  path('api/v1/tobaccos/create/', TobaccoCreateView.as_view(), name='tobaccos-create')
              ] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
