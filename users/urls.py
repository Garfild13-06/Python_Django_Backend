from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserProfileView

urlpatterns = [
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Djoser создаст набор необходимых элементов
    # Базовые, для управления пользователями в Django:
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/my_profile/', UserProfileView.as_view(), name='user-profile'),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]
