from django.urls import path

from bowls.views import BowlsListAPIView, BowlsDetailAPIView, BowlsCreateAPIView, BowlsUpdateAPIView, \
    BowlsPartialUpdateAPIView, BowlsDestroyAPIView

urlpatterns = ([
    path('api/v1/bowls/list/', BowlsListAPIView.as_view(), name='bowls-list'),
    path('api/v1/bowls/<uuid:pk>/', BowlsDetailAPIView.as_view(), name='bowls-detail'),
    path('api/v1/bowls/create/', BowlsCreateAPIView.as_view(), name='bowls-create'),
    path('api/v1/bowls/update/<uuid:pk>/', BowlsUpdateAPIView.as_view(), name='bowls-update'),
    path('api/v1/bowls/partial-update/<uuid:pk>/', BowlsPartialUpdateAPIView.as_view(), name='bowls-partial-update'),
    path('api/v1/bowls/delete/<uuid:pk>/', BowlsDestroyAPIView.as_view(), name='bowls-delete'),
])
