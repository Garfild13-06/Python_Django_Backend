from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from .models import TasteCategories
from .serializers import TasteCategoriesSerializer


class TasteCategoriesListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Получение списка категорий вкусов",
        operation_description=(
                "Возвращает список всех доступных категорий вкусов.\n\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Максимальное количество записей",
                                        example=10),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER, description="Смещение для пагинации", example=0),
            }
        ),
        responses={
            200: openapi.Response(
                description="Список категорий успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Список категорий успешно получен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "results": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="123e4567-e89b-12d3-a456-426614174000"),
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Фруктовые"),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=8),
                                "next": openapi.Schema(type=openapi.TYPE_STRING,
                                                       example="http://localhost:8000/api/v1/tastecategories/list/?limit=10&offset=10"),
                                "previous": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка в параметрах пагинации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Некорректные параметры пагинации"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Получение информации о категории вкусов по ID",
        operation_description=(
                "Возвращает детальную информацию о категории вкусов по её уникальному идентификатору.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        responses={
            200: openapi.Response(
                description="Детали категории успешно получены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Детали категории успешно получены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Фруктовые"),
                            }
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Категория не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Категория с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Создание новой категории вкусов",
        operation_description=(
                "Создаёт новую категорию вкусов с указанным названием.\n\n"
                "- Требуется поле `name`.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название категории", example="Фруктовые"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Категория успешно создана",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Категория успешно создана"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Фруктовые"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании категории",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при создании категории"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"name": ["This field is required"]})
                    }
                )
            ),
            401: openapi.Response(
                description="Не авторизован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуется аутентификация"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Полное обновление данных о категории вкусов",
        operation_description=(
                "Обновляет все поля категории вкусов по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название категории",
                                       example="Обновлённые Фруктовые"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Категория успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Категория успешно обновлена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённые Фруктовые"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении категории",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении категории"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"name": ["This field is required"]})
                    }
                )
            ),
            401: openapi.Response(
                description="Не авторизован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуется аутентификация"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Категория не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Категория с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Частичное обновление данных о категории вкусов",
        operation_description=(
                "Обновляет указанные поля категории вкусов по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название категории",
                                       example="Обновлённые Фруктовые"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Категория успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Категория успешно обновлена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённые Фруктовые"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении категории",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении категории"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT,
                                               example={"name": ["This field may not be blank"]})
                    }
                )
            ),
            401: openapi.Response(
                description="Не авторизован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуется аутентификация"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Категория не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Категория с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Категории вкусов'],
        operation_summary="Удаление категории вкусов",
        operation_description=(
                "Удаляет категорию вкусов по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        responses={
            204: openapi.Response(
                description="Категория успешно удалена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Категория успешно удалена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            401: openapi.Response(
                description="Не авторизован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуется аутентификация"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Категория не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Категория с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
