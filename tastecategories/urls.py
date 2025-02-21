# from django.urls import path
#
# from tastecategories.views import TasteCategoryCreateView
#
# urlpatterns = [
#     path('api/v1/taste-categories/create/', TasteCategoryCreateView.as_view(),
#          name='taste-categories-create')
# ]

from django.urls import path
from tastecategories.views import (
    TasteCategoriesListAPIView,
    TasteCategoriesDetailAPIView,
    TasteCategoriesCreateAPIView,
    TasteCategoriesUpdateAPIView,
    TasteCategoriesPartialUpdateAPIView,
    TasteCategoriesDestroyAPIView
)

urlpatterns = ([
    path('api/v1/tastecategories/list/', TasteCategoriesListAPIView.as_view(), name='tastecategories-list'),
    path('api/v1/tastecategories/<uuid:pk>/', TasteCategoriesDetailAPIView.as_view(), name='tastecategories-detail'),
    path('api/v1/tastecategories/create/', TasteCategoriesCreateAPIView.as_view(), name='tastecategories-create'),
    path('api/v1/tastecategories/update/<uuid:pk>/', TasteCategoriesUpdateAPIView.as_view(),
         name='tastecategories-update'),
    path('api/v1/tastecategories/partial-update/<uuid:pk>/', TasteCategoriesPartialUpdateAPIView.as_view(),
         name='tastecategories-partial-update'),
    path('api/v1/tastecategories/delete/<uuid:pk>/', TasteCategoriesDestroyAPIView.as_view(),
         name='tastecategories-delete'),
])
