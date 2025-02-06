from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Tobaccos, Mixes, Manufacturers, MixLikes, CustomUser, MixFavorites, TasteCategories
from main.serializers import CustomUserSerializer, MixesSerializer, \
    TobaccosListSerializer,CustomUserCreateSerializer, \
    CustomUserUpdateSerializer, TobaccosSerializer, TasteCategoriesSerializer


# Create your views here.
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Пользователь успешно зарегистрирован",
                "data": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при регистрации пользователя",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Нужен и email, и пароль",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({
                "status": "bad",
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Неверные данные",
                "data": None
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Вход выполнен успешно",
            "data": {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')  # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Необходим Refresh token",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавить его в чёрный список
        except Exception:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Неверный Refresh token",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Выход успешен",
            "data": None
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar.url if user.avatar else None,
            "date_joined": user.date_joined
        })

    def patch(self, request):
        """Частичное обновление профиля"""
        user = request.user
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "message": "Профиль успешно обновлён",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Ошибка обновления профиля",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "ok",
                "code": paginated_response.status_code,
                "message": "Список пользователей успешно получен",
                "data": paginated_response.data
            }, status=paginated_response.status_code)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список пользователей успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
def profile(request, user_id):
    pass


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """Кастомная офсетная пагинация."""

    max_limit = 100  # Максимально допустимое количество элементов

    def paginate_queryset(self, queryset, request, view=None):
        # Извлекаем параметры из тела запроса (body)
        limit = request.data.get('limit')
        offset = request.data.get('offset', 0)  # По умолчанию offset = 0

        if limit is None:
            limit = 10
        #     return Response({
        #         "status": "bad",
        #         "code": 400,
        #         "message": "Параметр 'limit' обязателен."
        #     }, status=400)

        try:
            self.limit = int(limit)
            self.offset = int(offset)
        except ValueError:
            return Response({
                "status": "bad",
                "code": 400,
                "message": "Некорректное значение для 'limit' или 'offset'."
            }, status=400)

        if self.limit > self.max_limit:
            return Response({
                "status": "bad",
                "code": 400,
                "message": f"Значение 'limit' не может превышать {self.max_limit}."
            }, status=400)

        self.count = queryset.count()
        self.request = request

        if self.offset >= self.count:
            return []

        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'count': self.count,
            'next_offset': self.offset + self.limit if self.offset + self.limit < self.count else None,
            'previous_offset': self.offset - self.limit if self.offset > 0 else None,
        })


# TobaccoViewSet
class TobaccoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Tobaccos.objects.all()
    serializer_class = TobaccosListSerializer
    pagination_class = CustomLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        search_query = request.data.get('search', None)

        if search_query:
            queryset = self.queryset.filter(
                Q(taste__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            queryset = self.queryset

        queryset = queryset.order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": 200,
            "message": "Список табаков успешно получен",
            "data": serializer.data
        }, status=200)


# 🔹 Создание микса
class MixCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Mixes.objects.all()
    serializer_class = MixesSerializer


# 🔹 Создание табака
class TobaccoCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tobaccos.objects.all()
    serializer_class = TobaccosSerializer


# 🔹 Создание категории вкусов
class TasteCategoryCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TasteCategories.objects.all()
    serializer_class = TasteCategoriesSerializer


# MixesListView
class MixesListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Mixes.objects.all()
        paginator = CustomLimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        if isinstance(paginated_queryset, Response):  # Проверяем на ошибочный ответ
            return paginated_queryset
        serializer = MixesSerializer(paginated_queryset, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MixesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": 201,
                "message": "Микс успешно создан",
                "data": serializer.data
            }, status=201)
        return Response({
            "status": "bad",
            "code": 400,
            "message": "Ошибка создания микса",
            "data": serializer.errors
        }, status=400)


class MixesViewSet(viewsets.ModelViewSet):
    queryset = Mixes.objects.all()
    serializer_class = MixesSerializer

    def get_serializer_context(self):
        # Здесь мы явно передаём request в контекст
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        # Логика для списка миксов с форматированием
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "ok",
                "code": paginated_response.status_code,
                "message": "Список миксов успешно получен",
                "data": paginated_response.data,
            }, status=paginated_response.status_code)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список миксов успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class MixDetailView(APIView):
    def get(self, request, mix_id, *args, **kwargs):
        mix = get_object_or_404(Mixes, id=mix_id)
        serializer = MixesSerializer(mix, context={'request': request})
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали микса успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class MixLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mix_id):
        mix = get_object_or_404(Mixes, id=mix_id)
        user = request.user
        like, created = MixLikes.objects.get_or_create(user=user, mix=mix)

        if not created:
            like.delete()
            return Response({
                "status": "ok",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Лайк удалён",
                "data": None
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "status": "ok",
            "code": status.HTTP_201_CREATED,
            "message": "Лайк добавлен",
            "data": None
        }, status=status.HTTP_201_CREATED)


class MixFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mix_id):
        mix = get_object_or_404(Mixes, id=mix_id)
        user = request.user
        favorite, created = MixFavorites.objects.get_or_create(user=user, mix=mix)

        if not created:
            favorite.delete()
            return Response({
                "status": "ok",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Удалено из избранного",
                "data": None
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "status": "ok",
            "code": status.HTTP_201_CREATED,
            "message": "Добавлено в избранное",
            "data": None
        }, status=status.HTTP_201_CREATED)
