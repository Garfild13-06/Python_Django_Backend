# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenRefreshView

# from users.views import UserProfileView

# urlpatterns = [
# # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# # Djoser создаст набор необходимых элементов
# # Базовые, для управления пользователями в Django:
# path('api/v1/auth/', include('djoser.urls')),
# path('api/v1/my_profile/', UserProfileView.as_view(), name='user-profile'),
# # JWT-эндпоинты, для управления JWT-токенами:
# path('api/v1/', include('djoser.urls.jwt')),
# path('api/v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh')
# ]

from django.urls import path
from users.views import (
    UserListAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    UserPartialUpdateAPIView,
    UserDeleteAPIView, UserProfileView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Пользователи
    path('api/v1/users/list/', UserListAPIView.as_view(), name='user-list'),
    path('api/v1/users/detail/', UserDetailAPIView.as_view(), name='user-detail'),
    path('api/v1/users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('api/v1/users/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('api/v1/users/partial-update/', UserPartialUpdateAPIView.as_view(), name='user-partial-update'),
    path('api/v1/users/delete/', UserDeleteAPIView.as_view(), name='user-delete'),

    # Профиль пользователя
    path('api/v1/my_profile/', UserProfileView.as_view(), name='user-profile'),

    # Токены
    path('api/v1/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('api/v1/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('api/v1/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
