from django.urls import path
from manufacturers.views import ManufacturersCreateAPIView, ManufacturersListAPIView, ManufacturersDetailAPIView, \
    ManufacturersUpdateAPIView, ManufacturersPartialUpdateAPIView, ManufacturersDestroyAPIView

urlpatterns = [
    path('api/v1/manufacturers/list/', ManufacturersListAPIView.as_view(), name='manufacturers-list'),
    path('api/v1/manufacturers/<uuid:pk>/', ManufacturersDetailAPIView.as_view(), name='manufacturers-detail'),
    path('api/v1/manufacturers/create/', ManufacturersCreateAPIView.as_view(), name='manufacturers-create'),
    path('api/v1/manufacturers/update/<uuid:pk>/', ManufacturersUpdateAPIView.as_view(), name='manufacturers-update'),
    path('api/v1/manufacturers/partial-update/<uuid:pk>/', ManufacturersPartialUpdateAPIView.as_view(),
         name='manufacturers-partial-update'),
    path('api/v1/manufacturers/delete/<uuid:pk>/', ManufacturersDestroyAPIView.as_view(), name='manufacturers-delete'),
]
