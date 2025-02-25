from django.urls import path

from mixes.views import *

urlpatterns = [
    path('api/v1/mixes/list/', MixesListAPIView.as_view(), name='mixes-list'),
    path('api/v1/mixes/detail/', MixDetailView.as_view(), name='mix-detail'),
    path('api/v1/mixes/create/', MixesCreateAPIView.as_view(), name='mix-create'),
    path('api/v1/mixes/update/', MixUpdateAPIView.as_view(), name='mix-update'),
    path('api/v1/mixes/partial-update/', MixesPartialUpdateAPIView.as_view(), name='mix-partial-update'),
    path('api/v1/mixes/delete/', MixDestroyAPIView.as_view(), name='mix-delete'),
    path('api/v1/mixes/likes/', MixLikeAPIView.as_view(), name='mix-like'),
    path('api/v1/mixes/favorites/', MixFavoriteAPIView.as_view(), name='mix-favorite'),
    path('api/v1/user/liked-mixes/', UserLikedMixesView.as_view(), name='user-liked-mixes'),
    path('api/v1/user/favorited-mixes/', UserFavoritedMixesView.as_view(), name='user-favorite-mixes'),
    path('api/v1/mixes/contained/', MixesContainedAPIView.as_view(), name='mixes-contained'),
]
