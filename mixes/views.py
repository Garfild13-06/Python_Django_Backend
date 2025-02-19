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

from users.views import CustomLimitOffsetPagination
from mixes.models import Mixes, MixLikes, MixFavorites
from mixes.serializers import MixesSerializer


# Create your views here.
# 🔹 Создание микса
class MixCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Mixes.objects.all()
    serializer_class = MixesSerializer

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