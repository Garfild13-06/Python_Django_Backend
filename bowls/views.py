from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Bowls
from .serializers import BowlsSerializer


class BowlsListAPIView(APIView):
    """
    Обработка POST-запроса для получения списка чаш.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Получение списка чаш"
    )
    def post(self, request, *args, **kwargs):
        queryset = Bowls.objects.all()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = BowlsSerializer(page, many=True)
            return paginator.get_paginated_response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Список чаш успешно получен",
                "data": serializer.data
            })
        serializer = BowlsSerializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список чаш успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class BowlsDetailAPIView(APIView):
    """
    Обработка POST-запроса для получения деталей чаши по её ID.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Получение информации о чаще по id"
    )
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Bowls, pk=pk)
        serializer = BowlsSerializer(instance)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали чаши успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class BowlsCreateAPIView(APIView):
    """
    Обработка POST-запроса для создания новой чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Создание новой чаши"
    )
    def post(self, request, *args, **kwargs):
        serializer = BowlsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Чаша успешно создана",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при создании чаши",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BowlsUpdateAPIView(APIView):
    """
    Обработка PUT-запроса для полного обновления чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Полное обновление данных о чаше по id"
    )
    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Bowls, pk=pk)
        serializer = BowlsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Чаша успешно обновлена",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении чаши",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BowlsPartialUpdateAPIView(APIView):
    """
    Обработка PATCH-запроса для частичного обновления чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Частичное обновление данных о чаше по id"
    )
    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Bowls, pk=pk)
        serializer = BowlsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Чаша успешно обновлена",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении чаши",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BowlsDestroyAPIView(APIView):
    """
    Обработка DELETE-запроса для удаления чаши.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Удаление чаши по id"
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Bowls, pk=pk)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Чаша успешно удалена",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)
