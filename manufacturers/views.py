from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, filters
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from main.models import Manufacturers
from manufacturers.serializers import ManufacturersSerializer


class ManufacturersListAPIView(APIView):
    """
    Обработка POST-запроса для получения списка чаш.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Получение списка производителей"
    )
    def post(self, request, *args, **kwargs):
        queryset = Manufacturers.objects.all()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ManufacturersSerializer(page, many=True)
            return paginator.get_paginated_response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Список производителей успешно получен",
                "data": serializer.data
            })
        serializer = ManufacturersSerializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список производителей успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class ManufacturersDetailAPIView(APIView):
    """
    Обработка POST-запроса для получения деталей производителя по его ID.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Получение информации о производителе по id"
    )
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Manufacturers, pk=pk)
        serializer = ManufacturersSerializer(instance)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали производителя успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# 🔹 Создание производителя
class ManufacturersCreateAPIView(APIView):
    """
    Обработка POST-запроса для создания нового производителя.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Создание нового производителя",
        operation_description="Создает нового производителя. Требует аутентификации по токену.",
    )
    def post(self, request, *args, **kwargs):
        serializer = ManufacturersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Производитель успешно создан",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при создании производителя",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ManufacturersUpdateAPIView(APIView):
    """
    Обработка PUT-запроса для полного обновления чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Полное обновление данных о производителе по id"
    )
    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Manufacturers, pk=pk)
        serializer = ManufacturersSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Производитель успешно обновлён",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении производителя",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ManufacturersPartialUpdateAPIView(APIView):
    """
    Обработка PATCH-запроса для частичного обновления чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Частичное обновление данных о производителе по id"
    )
    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Manufacturers, pk=pk)
        serializer = ManufacturersSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Производитель успешно обновлён",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении производителя",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ManufacturersDestroyAPIView(APIView):
    """
    Обработка DELETE-запроса для удаления производителя.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Удаление производителя по id"
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Manufacturers, pk=pk)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Производитель успешно удалена",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)