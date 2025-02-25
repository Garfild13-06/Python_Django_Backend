from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import Manufacturers
from .serializers import ManufacturersSerializer


class ManufacturersListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Получение списка производителей",
        operation_description=(
                "Возвращает список всех доступных производителей.\n\n"
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
                description="Список производителей успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Список производителей успешно получен"),
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
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="DarkSide"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Производитель премиум-табака"),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/manufacturers/darkside.jpg"),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                "next": openapi.Schema(type=openapi.TYPE_STRING,
                                                       example="http://localhost:8000/api/v1/manufacturers/list/?limit=10&offset=10"),
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
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Получение информации о производителе по ID",
        operation_description=(
                "Возвращает детальную информацию о производителе по его уникальному идентификатору.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        responses={
            200: openapi.Response(
                description="Детали производителя успешно получены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Детали производителя успешно получены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="DarkSide"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Производитель премиум-табака"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/manufacturers/darkside.jpg"),
                            }
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Производитель не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Производитель с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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


class ManufacturersCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Создание нового производителя",
        operation_description=(
                "Создаёт нового производителя с указанными данными.\n\n"
                "- Требуются поля `name`, `description` (опционально), `image` (опционально).\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название производителя",
                                       example="DarkSide"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание производителя",
                                              example="Производитель премиум-табака"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение производителя (опционально)"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Производитель успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Производитель успешно создан"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="DarkSide"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Производитель премиум-табака"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/manufacturers/darkside.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании производителя",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Ошибка при создании производителя"),
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Полное обновление данных о производителе",
        operation_description=(
                "Обновляет все поля производителя по его ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название производителя",
                                       example="Updated DarkSide"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание производителя",
                                              example="Обновлённое описание"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение производителя (опционально)"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Производитель успешно обновлён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Производитель успешно обновлён"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Updated DarkSide"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённое описание"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/manufacturers/updated_darkside.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении производителя",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Ошибка при обновлении производителя"),
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
                description="Производитель не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Производитель с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Частичное обновление данных о производителе",
        operation_description=(
                "Обновляет указанные поля производителя по его ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название производителя",
                                       example="Updated DarkSide"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание производителя",
                                              example="Обновлённое описание"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение производителя (опционально)"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Производитель успешно обновлён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Производитель успешно обновлён"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Updated DarkSide"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённое описание"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/manufacturers/updated_darkside.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении производителя",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Ошибка при обновлении производителя"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT,
                                               example={"description": ["This field may not be blank"]})
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
                description="Производитель не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Производитель с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Производители'],
        operation_summary="Удаление производителя",
        operation_description=(
                "Удаляет производителя по его ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        responses={
            204: openapi.Response(
                description="Производитель успешно удалён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Производитель успешно удалён"),
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
                description="Производитель не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Производитель с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Manufacturers, pk=pk)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Производитель успешно удалён",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)
