from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from tobaccos.models import Tobaccos
from .models import Mixes, MixLikes, MixFavorites
from utils.CustomLimitOffsetPagination import CustomLimitOffsetPagination
from .serializers import MixesListSerializer, MixesDetailSerializer, MixesSerializer


class MixesListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка миксов",
        operation_description=(
                "Возвращает список всех доступных миксов.\n\n"
                "- Поддерживает поиск по полю `search` (имя или описание).\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search': openapi.Schema(type=openapi.TYPE_STRING, description="Поиск по имени или описанию",
                                         example="Fruit"),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Максимальное количество записей",
                                        example=10),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER, description="Смещение для пагинации", example=0),
            }
        ),
        responses={
            200: openapi.Response(
                description="Список миксов успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Список миксов успешно получен"),
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
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Сочный фруктовый микс"),
                                            "banner": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                            "created": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      format=openapi.FORMAT_DATETIME,
                                                                      example="2023-01-01T12:00:00Z"),
                                            "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=20),
                                "next_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "previous_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка в параметрах запроса",
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
        queryset = Mixes.objects.all()
        search_query = request.data.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(
                description__icontains=search_query)
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = MixesListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class MixDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение информации о миксе по ID",
        operation_description=(
                "Возвращает детальную информацию о миксе по его уникальному идентификатору.\n\n"
                "- Требуется передать `id` в теле запроса.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                     example="123e4567-e89b-12d3-a456-426614174000"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Детали микса успешно получены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Детали микса успешно получены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Сочный фруктовый микс"),
                                "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                         example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                          example="2023-01-01T12:00:00Z"),
                                "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Некорректные данные",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'id' обязательно"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        mix_id = request.data.get('id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'id' обязательно", "data": None},
                            status=400)
        instance = get_object_or_404(Mixes, pk=mix_id)
        serializer = MixesDetailSerializer(instance, context={'request': request})
        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали микса успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class MixesCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Создание нового микса",
        operation_description=(
                "Создаёт новый микс с указанными данными.\n\n"
                "- Требуются поля `name`, остальные опциональны.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название микса", example="Fruit Mix"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание микса",
                                              example="Сочный фруктовый микс"),
                "tasteType": openapi.Schema(type=openapi.TYPE_STRING, description="Тип вкуса", example="fruit"),
                "banner": openapi.Schema(type=openapi.TYPE_FILE, description="Баннер микса (опционально)"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Микс успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно создан"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Сочный фруктовый микс"),
                                "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                         example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                          example="2023-01-01T12:00:00Z"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании микса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при создании микса"),
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
        serializer = MixesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Микс успешно создан",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при создании микса",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MixUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Полное обновление данных о миксе",
        operation_description=(
                "Обновляет все поля микса по его ID.\n\n"
                "- Требуется передать `mix_id` в теле запроса.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mix_id'],
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                         example="123e4567-e89b-12d3-a456-426614174000"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название микса",
                                       example="Updated Fruit Mix"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание микса",
                                              example="Обновлённый фруктовый микс"),
                "tasteType": openapi.Schema(type=openapi.TYPE_STRING, description="Тип вкуса", example="sweet"),
                "banner": openapi.Schema(type=openapi.TYPE_FILE, description="Баннер микса (опционально)"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Микс успешно обновлён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно обновлён"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Fruit Mix"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Обновлённый фруктовый микс"),
                                "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                         example="http://localhost:8000/media/mixes/updated_fruit_mix.jpg"),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                          example="2023-01-01T12:00:00Z"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении микса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении микса"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"mix_id": ["This field is required"]})
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
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def put(self, request, *args, **kwargs):
        mix_id = request.data.get('mix_id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'mix_id' обязательно", "data": None},
                            status=400)
        instance = get_object_or_404(Mixes, pk=mix_id)
        serializer = MixesSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Микс успешно обновлён",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении микса",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MixesPartialUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Частичное обновление данных о миксе",
        operation_description=(
                "Обновляет указанные поля микса по его ID.\n\n"
                "- Требуется передать `mix_id` в теле запроса.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                         example="123e4567-e89b-12d3-a456-426614174000"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название микса",
                                       example="Updated Fruit Mix"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание микса",
                                              example="Обновлённое описание"),
                "tasteType": openapi.Schema(type=openapi.TYPE_STRING, description="Тип вкуса", example="sweet"),
                "banner": openapi.Schema(type=openapi.TYPE_FILE, description="Баннер микса (опционально)"),
            },
            required=['mix_id']
        ),
        responses={
            200: openapi.Response(
                description="Микс успешно обновлён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно обновлён"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Fruit Mix"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённое описание"),
                                "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                         example="http://localhost:8000/media/mixes/updated_fruit_mix.jpg"),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                          example="2023-01-01T12:00:00Z"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении микса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении микса"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"mix_id": ["This field is required"]})
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
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        mix_id = request.data.get('mix_id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'mix_id' обязательно", "data": None},
                            status=400)
        instance = get_object_or_404(Mixes, pk=mix_id)
        serializer = MixesSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Микс успешно обновлён",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении микса",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MixDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Удаление микса",
        operation_description=(
                "Удаляет микс по его ID.\n\n"
                "- Требуется передать `mix_id` в теле запроса.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mix_id'],
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                         example="123e4567-e89b-12d3-a456-426614174000"),
            }
        ),
        responses={
            204: openapi.Response(
                description="Микс успешно удалён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно удалён"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            400: openapi.Response(
                description="Некорректные данные",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'mix_id' обязательно"),
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
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        mix_id = request.data.get('mix_id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'mix_id' обязательно", "data": None},
                            status=400)
        instance = get_object_or_404(Mixes, pk=mix_id)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Микс успешно удалён",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)


class MixLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Добавление/удаление лайка для микса",
        operation_description=(
                "Добавляет или убирает лайк для микса.\n\n"
                "- Требуется передать `mix_id` в теле запроса.\n"
                "- Если лайк уже есть, он будет удалён, если нет — добавлен.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mix_id'],
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                         example="123e4567-e89b-12d3-a456-426614174000"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Лайк успешно добавлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Лайк успешно добавлен"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            204: openapi.Response(
                description="Лайк успешно удалён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Лайк успешно удалён"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            400: openapi.Response(
                description="Некорректные данные",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'mix_id' обязательно"),
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
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        mix_id = request.data.get('mix_id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'mix_id' обязательно", "data": None},
                            status=400)
        mix = get_object_or_404(Mixes, pk=mix_id)
        like = MixLikes.objects.filter(mix=mix, user=request.user).first()
        if like:
            like.delete()
            return Response({"status": "ok", "code": 204, "message": "Лайк успешно удалён", "data": None}, status=204)
        else:
            MixLikes.objects.create(mix=mix, user=request.user)
            return Response({"status": "ok", "code": 201, "message": "Лайк успешно добавлен", "data": None}, status=201)


class MixFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Добавление/удаление микса в избранное",
        operation_description=(
                "Добавляет или убирает микс из избранного.\n\n"
                "- Требуется передать `mix_id` в теле запроса.\n"
                "- Если микс уже в избранном, он будет удалён, если нет — добавлен.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mix_id'],
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID микса",
                                         example="123e4567-e89b-12d3-a456-426614174000"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Микс успешно добавлен в избранное",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс успешно добавлен в избранное"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            204: openapi.Response(
                description="Микс успешно удалён из избранного",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс успешно удалён из избранного"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            400: openapi.Response(
                description="Некорректные данные",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'mix_id' обязательно"),
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
                description="Микс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        mix_id = request.data.get('mix_id')
        if not mix_id:
            return Response({"status": "bad", "code": 400, "message": "Поле 'mix_id' обязательно", "data": None},
                            status=400)
        mix = get_object_or_404(Mixes, pk=mix_id)
        favorite = MixFavorites.objects.filter(mix=mix, user=request.user).first()
        if favorite:
            favorite.delete()
            return Response({"status": "ok", "code": 204, "message": "Микс успешно удалён из избранного", "data": None},
                            status=204)
        else:
            MixFavorites.objects.create(mix=mix, user=request.user)
            return Response({"status": "ok", "code": 201, "message": "Микс успешно добавлен в избранное", "data": None},
                            status=201)


class UserLikedMixesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка лайкнутых миксов пользователя",
        operation_description=(
                "Возвращает список миксов, которые текущий пользователь лайкнул.\n\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`.\n"
                "- Требуется аутентификация через JWT."
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
                description="Список лайкнутых миксов успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Список лайкнутых миксов успешно получен"),
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
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Сочный фруктовый микс"),
                                            "banner": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                            "created": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      format=openapi.FORMAT_DATETIME,
                                                                      example="2023-01-01T12:00:00Z"),
                                            "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                            "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                "next_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "previous_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
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
        liked_mixes = Mixes.objects.filter(likes__user=request.user)
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(liked_mixes, request)
        serializer = MixesSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class UserFavoritedMixesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка избранных миксов пользователя",
        operation_description=(
                "Возвращает список миксов, добавленных текущим пользователем в избранное.\n\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`.\n"
                "- Требуется аутентификация через JWT."
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
                description="Список избранных миксов успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Список избранных миксов успешно получен"),
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
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Сочный фруктовый микс"),
                                            "banner": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                            "created": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      format=openapi.FORMAT_DATETIME,
                                                                      example="2023-01-01T12:00:00Z"),
                                            "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
                                "next_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "previous_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
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
        favorited_mixes = Mixes.objects.filter(favorites__user=request.user)
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(favorited_mixes, request)
        serializer = MixesSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class MixesContainedAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка миксов, содержащих указанный табак",
        operation_description=(
                "Возвращает пагинированный список миксов, которые содержат табак с указанным ID.\n\n"
                "- Требуется передать `id` табака в теле запроса.\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_UUID,
                    description="ID табака",
                    example="123e4567-e89b-12d3-a456-426614174000"
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Максимальное количество записей",
                    example=10
                ),
                'offset': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Смещение для пагинации",
                    example=0
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Список миксов успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Mixes containing the tobacco retrieved successfully"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "results": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="550e8400-e29b-41d4-a716-446655440000"),
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Сочный фруктовый микс"),
                                            "banner": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                            "created": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      format=openapi.FORMAT_DATETIME,
                                                                      example="2023-01-01T12:00:00Z"),
                                            "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "categories": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                             format=openapi.FORMAT_UUID,
                                                                             example="123e4567-e89b-12d3-a456-426614174000"),
                                                        "name": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="Фруктовые")
                                                    }
                                                )
                                            ),
                                            "goods": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        "tobacco": openapi.Schema(
                                                            type=openapi.TYPE_OBJECT,
                                                            properties={
                                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                     format=openapi.FORMAT_UUID,
                                                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                                                "taste": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                        example="Apple"),
                                                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                               example="DarkSide"),
                                                                "image": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                        format=openapi.FORMAT_URI,
                                                                                        example="http://localhost:8000/media/tobaccos/apple.jpg")
                                                            }
                                                        ),
                                                        "weight": openapi.Schema(type=openapi.TYPE_INTEGER, example=10)
                                                    }
                                                )
                                            ),
                                            "author": openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                         format=openapi.FORMAT_UUID,
                                                                         example="123e4567-e89b-12d3-a456-426614174000"),
                                                    "email": openapi.Schema(type=openapi.TYPE_STRING,
                                                                            example="author@example.com"),
                                                    "username": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="author123"),
                                                    "nickname": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="Author"),
                                                    "avatar": openapi.Schema(type=openapi.TYPE_STRING,
                                                                             format=openapi.FORMAT_URI,
                                                                             example="http://localhost:8000/media/avatars/author.jpg"),
                                                    "date_joined": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                  format=openapi.FORMAT_DATETIME,
                                                                                  example="2023-01-01T12:00:00Z")
                                                }
                                            )
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "next_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "previous_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Некорректные данные в теле запроса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Tobacco ID is required"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Табак не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Tobacco not found"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request):
        tobacco_id = request.data.get('id')
        if not tobacco_id:
            return Response({"status": "bad", "code": 400, "message": "Tobacco ID is required", "data": None},
                            status=400)

        try:
            tobacco = Tobaccos.objects.get(id=tobacco_id)
        except (ValueError, Tobaccos.DoesNotExist):
            return Response({"status": "bad", "code": 404, "message": "Tobacco not found", "data": None}, status=404)

        mixes = Mixes.objects.filter(compares__tobacco=tobacco)

        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(mixes, request)
        context = {'request': request}
        serializer = MixesListSerializer(page, many=True, context=context)
        return paginator.get_paginated_response(serializer.data)


class MixesByAuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка миксов по ID автора",
        operation_description=
        "Возвращает список миксов, созданных пользователем с указанным ID. Доступно только авторизованным пользователям через JWT.\n"
        "- Требуется поле`author_id`.\n"
        "- Поддерживает пагинацию через параметры `limit` и `offset`.\n",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['author_id'],
            properties={
                'author_id': openapi.Schema(type=openapi.TYPE_STRING, description="ID автора",
                                            example="123e4567-e89b-12d3-a456-426614174000"),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Максимальное количество записей",
                                        example=10),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER, description="Смещение для пагинации", example=0),
            }
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Список миксов успешно получен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "results": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                 example="550e8400-e29b-41d4-a716-446655440000"),
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit Mix"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Сочный фруктовый микс"),
                                            "banner": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     example="http://localhost:8000/media/mixes/fruit_mix.jpg"),
                                            "created": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      example="2023-01-01T12:00:00Z"),
                                            "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                                            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                            "categories": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                                                type=openapi.TYPE_OBJECT)),
                                            "goods": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                    items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                                            "author": openapi.Schema(type=openapi.TYPE_OBJECT),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                                "next_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                "previous_offset": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description="Ошибка: author_id не указан"),
            401: openapi.Response(description="Ошибка: не авторизован"),
        }
    )
    def post(self, request):
        author_id = request.data.get('author_id')
        if not author_id:
            return Response({
                "status": "bad",
                "code": 400,
                "message": "Author ID is required",
                "data": None
            }, status=400)

        # Фильтрация миксов по автору
        mixes = Mixes.objects.filter(author_id=author_id)

        # Пагинация (если используется в проекте)
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(mixes, request)

        # Сериализация данных
        serializer = MixesListSerializer(page, many=True, context={'request': request})

        # Формирование ответа с пагинацией
        return paginator.get_paginated_response(serializer.data)
