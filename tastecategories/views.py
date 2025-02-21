# from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from tastecategories.models import TasteCategories
# from tastecategories.serializers import TasteCategoriesSerializer
#
#
# class TasteCategoryCreateView(CreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = TasteCategories.objects.all()
#     serializer_class = TasteCategoriesSerializer

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from tastecategories.models import TasteCategories
from tastecategories.serializers import TasteCategoriesSerializer

class TasteCategoriesListAPIView(APIView):
    """
    Получение списка категорий вкусов.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Получение списка категорий вкусов"
    )
    def post(self, request, *args, **kwargs):
        queryset = TasteCategories.objects.all()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = TasteCategoriesSerializer(page, many=True)
            return paginator.get_paginated_response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Список категорий успешно получен",
                "data": serializer.data
            })
        serializer = TasteCategoriesSerializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список категорий успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class TasteCategoriesDetailAPIView(APIView):
    """
    Получение деталей категории вкусов по ID.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Получение информации о категории вкусов по ID"
    )
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(TasteCategories, pk=pk)
        serializer = TasteCategoriesSerializer(instance)
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали категории успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class TasteCategoriesCreateAPIView(APIView):
    """
    Создание новой категории вкусов.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Создание новой категории вкусов"
    )
    def post(self, request, *args, **kwargs):
        serializer = TasteCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Категория успешно создана",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при создании категории",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TasteCategoriesUpdateAPIView(APIView):
    """
    Полное обновление категории вкусов.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Полное обновление категории вкусов по ID"
    )
    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(TasteCategories, pk=pk)
        serializer = TasteCategoriesSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Категория успешно обновлена",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении категории",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TasteCategoriesPartialUpdateAPIView(APIView):
    """
    Частичное обновление категории вкусов.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Частичное обновление категории вкусов по ID"
    )
    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(TasteCategories, pk=pk)
        serializer = TasteCategoriesSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Категория успешно обновлена",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении категории",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TasteCategoriesDestroyAPIView(APIView):
    """
    Удаление категории вкусов.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Удаление категории вкусов по ID"
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(TasteCategories, pk=pk)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Категория успешно удалена",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)