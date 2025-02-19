from django.urls import path

from tastecategories.views import TasteCategoryCreateView

urlpatterns = [
    path('api/v1/taste-categories/create/', TasteCategoryCreateView.as_view(),
         name='taste-categories-create')
]
