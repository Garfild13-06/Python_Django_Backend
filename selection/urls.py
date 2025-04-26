from django.urls import path
from selection.views import SelectionOptionsAPIView, TobaccosByManufacturerAPIView

urlpatterns = [
    path('api/v1/selection/options/', SelectionOptionsAPIView.as_view(), name='selection-options'),
    path('api/v1/selection/tobaccos-by-manufacturer/', TobaccosByManufacturerAPIView.as_view(), name='tobaccos-by-manufacturer'),
]
