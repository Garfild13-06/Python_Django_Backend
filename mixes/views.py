from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from utils.CustomLimitOffsetPagination import CustomLimitOffsetPagination
from .models import Mixes, MixLikes, MixFavorites
from .serializers import MixesSerializer


class MixesListAPIView(APIView):
    """
    Обработка POST-запроса для получения списка миксов.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка миксов",
        operation_description=(
                "Возвращает список всех доступных миксов.\n\n"
                "- Поддерживает поиск по полю `name` через параметр `search`.\n\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`."
        ),
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Текст для поиска по названию микса",
                required=False
            ),
            openapi.Parameter(
                name='limit',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Максимальное количество элементов на странице",
                default=10,
                required=False
            ),
            openapi.Parameter(
                name='offset',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Смещение для пагинации",
                default=0,
                required=False
            ),
        ],
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
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                         example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test Mix"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                  example="A delicious mix of flavors."),
                                    "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                             example="http://localhost:8000/media/mix_banner.jpg"),
                                    "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-10-01T12:00:00Z"),
                                    "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=42),
                                    "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                    "categories": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit"),
                                            }
                                        )
                                    ),
                                    "goods": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Apple"),
                                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="Reyes-Ryan"),
                                                "image": openapi.Schema(type=openapi.TYPE_STRING,
                                                                        format=openapi.FORMAT_URI,
                                                                        example="http://localhost:8000/media/tobacco_image.jpg"),
                                                "weight": openapi.Schema(type=openapi.TYPE_INTEGER, example=50),
                                            }
                                        )
                                    ),
                                    "bowl": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                            "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="A bowl with a single hole in the center."),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/bowl_image.jpg"),
                                        }
                                    ),
                                    "author": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="123e4567-e89b-12d3-a456-426614174000"),
                                            "username": openapi.Schema(type=openapi.TYPE_STRING, example="testuser"),
                                            "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                                            "avatar": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/avatar.jpg"),
                                        }
                                    ),
                                }
                            )
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
                        "errors": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        # Извлекаем параметр 'search' из тела запроса
        search_query = request.data.get('search', None)

        # Формируем базовый QuerySet
        queryset = Mixes.objects.all()

        # Если передан параметр 'search', фильтруем QuerySet
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Пагинация
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        # Сериализация данных
        serializer = MixesSerializer(
            page if page is not None else queryset,
            many=True,
            context={'request': request}  # Передаем request для формирования абсолютных ссылок
        )

        # Возвращаем пагинированный или полный ответ
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список миксов успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class MixDetailView(APIView):
    """
    Получение деталей микса по ID, переданному в теле запроса.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Миксы'],  # Группа операций в Swagger
        operation_summary="Получение информации о миксе по ID",
        operation_description=(
                "Возвращает детальную информацию о миксе по его уникальному идентификатору.\n\n"
                "- Требуется передать `id` в теле запроса."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_UUID,
                    example="82b74c74-2399-405a-83af-26761b6fcd5b"
                ),
            },
            required=["id"],
        ),
        responses={
            200: openapi.Response(
                description="Информация о миксе успешно получена",
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
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test Mix"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="A delicious mix of flavors."),
                                "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                         example="http://localhost:8000/media/mix_banner.jpg"),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                          example="2023-10-01T12:00:00Z"),
                                "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=42),
                                "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                "categories": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="123e4567-e89b-12d3-a456-426614174000"),
                                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit"),
                                        }
                                    )
                                ),
                                "goods": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                            "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Apple"),
                                            "manufacturer": openapi.Schema(type=openapi.TYPE_STRING,
                                                                           example="Reyes-Ryan"),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/tobacco_image.jpg"),
                                            "weight": openapi.Schema(type=openapi.TYPE_INTEGER, example=50),
                                        }
                                    )
                                ),
                                "bowl": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                             example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                        "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                        "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                      example="A bowl with a single hole in the center."),
                                        "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                example="http://localhost:8000/media/bowl_image.jpg"),
                                    }
                                ),
                                "author": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                             example="123e4567-e89b-12d3-a456-426614174000"),
                                        "username": openapi.Schema(type=openapi.TYPE_STRING, example="testuser"),
                                        "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                                        "avatar": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                 example="http://localhost:8000/media/avatar.jpg"),
                                    }
                                ),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Поле 'id' обязательно для заполнения"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        # Извлекаем ID микса из тела запроса
        mix_id = request.data.get("id")
        if not mix_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Получаем объект микса или возвращаем 404, если он не существует
        mix = get_object_or_404(Mixes, id=mix_id)
        serializer = MixesSerializer(mix, context={'request': request})

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Детали микса успешно получены",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class MixesCreateAPIView(APIView):
    """
    Создание нового микса.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Создание нового микса",
        request_body=MixesSerializer,
        responses={
            201: MixesSerializer(),
            400: "Ошибка при создании микса",
            401: "Не авторизован"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = MixesSerializer(data=request.data, context={'request': request})
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
    """
    Обработка PUT-запроса для полного обновления микса.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Полное обновление данных о миксе",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                         example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Mix Name"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Updated description"),
                "banner": openapi.Schema(type=openapi.TYPE_FILE, example="image.jpg"),
                "categories": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
                    example=["123e4567-e89b-12d3-a456-426614174000", "82b74c74-2399-405a-83af-26761b6fcd5b"]
                ),
                "tasteType": openapi.Schema(type=openapi.TYPE_STRING, example="fruit"),
            },
            required=["mix_id"]
        ),
        responses={
            200: openapi.Response(
                description="Микс успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно обновлен"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении микса"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        mix_id = request.data.get("mix_id")
        if not mix_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'mix_id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        mix = get_object_or_404(Mixes, id=mix_id)
        serializer = MixesSerializer(mix, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Микс успешно обновлен",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении микса",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MixesPartialUpdateAPIView(APIView):
    """
    Частичное обновление микса.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Частичное обновление микса по ID",
        request_body=MixesSerializer(partial=True),
        responses={
            200: MixesSerializer(),
            400: "Ошибка при обновлении микса",
            401: "Не авторизован",
            404: "Микс не найден"
        }
    )
    def patch(self, request, pk, *args, **kwargs):
        instance = Mixes.objects.get(pk=pk)
        serializer = MixesSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Микс успешно обновлен",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении микса",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MixDestroyAPIView(APIView):
    """
    Обработка DELETE-запроса для удаления микса.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Удаление микса",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                         example="82b74c74-2399-405a-83af-26761b6fcd5b")
            },
            required=["mix_id"]
        ),
        responses={
            204: openapi.Response(
                description="Микс успешно удален",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Микс успешно удален"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Некорректный формат данных"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        mix_id = request.data.get("mix_id")
        if not mix_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'mix_id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        mix = get_object_or_404(Mixes, id=mix_id)
        mix.delete()

        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Микс успешно удален",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)


class MixLikeAPIView(APIView):
    """
    Обработка POST-запроса для добавления или удаления лайка к миксу.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Добавление или удаление лайка к миксу",
        operation_description=(
                "Этот эндпоинт позволяет пользователю добавить или удалить лайк к миксу.\n\n"
                "- Если лайк уже существует, он будет удален.\n"
                "- Если лайка нет, он будет создан."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                         example="82b74c74-2399-405a-83af-26761b6fcd5b")
            },
            required=["mix_id"]
        ),
        responses={
            201: openapi.Response(
                description="Лайк успешно добавлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Лайк добавлен"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            204: openapi.Response(
                description="Лайк успешно удален",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Лайк удален"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Authentication credentials were not provided."),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        mix_id = request.data.get("mix_id")
        if not mix_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'mix_id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        mix = get_object_or_404(Mixes, id=mix_id)
        user = request.user
        like, created = MixLikes.objects.get_or_create(user=user, mix=mix)

        if not created:
            like.delete()
            return Response({
                "status": "ok",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Лайк удален",
                "data": None
            }, status=status.HTTP_204_NO_CONTENT)

        return Response({
            "status": "ok",
            "code": status.HTTP_201_CREATED,
            "message": "Лайк добавлен",
            "data": None
        }, status=status.HTTP_201_CREATED)


class MixFavoriteAPIView(APIView):
    """
    Обработка POST-запроса для добавления или удаления микса из избранного.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Добавление или удаление микса из избранного",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mix_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                         example="82b74c74-2399-405a-83af-26761b6fcd5b")
            },
            required=["mix_id"]
        ),
        responses={
            201: openapi.Response(
                description="Микс успешно добавлен в избранное",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Добавлено в избранное"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            204: openapi.Response(
                description="Микс успешно удален из избранного",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Удалено из избранного"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Некорректный формат данных"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Микс с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        mix_id = request.data.get("mix_id")
        if not mix_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'mix_id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

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


class UserLikedMixesView(APIView):
    """
    Получение списка миксов, которые лайкнул текущий пользователь.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка лайкнутых миксов текущим пользователем",
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
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                         example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test Mix"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                  example="A delicious mix of flavors."),
                                    "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                             example="http://localhost:8000/media/mix_banner.jpg"),
                                    "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-10-01T12:00:00Z"),
                                    "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=42),
                                    "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                    "categories": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit"),
                                            }
                                        )
                                    ),
                                    "goods": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Apple"),
                                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="Reyes-Ryan"),
                                                "image": openapi.Schema(type=openapi.TYPE_STRING,
                                                                        format=openapi.FORMAT_URI,
                                                                        example="http://localhost:8000/media/tobacco_image.jpg"),
                                                "weight": openapi.Schema(type=openapi.TYPE_INTEGER, example=50),
                                            }
                                        )
                                    ),
                                    "bowl": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                            "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="A bowl with a single hole in the center."),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/bowl_image.jpg"),
                                        }
                                    ),
                                    "author": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="123e4567-e89b-12d3-a456-426614174000"),
                                            "username": openapi.Schema(type=openapi.TYPE_STRING, example="testuser"),
                                            "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                                            "avatar": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/avatar.jpg"),
                                        }
                                    ),
                                }
                            )
                        )
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Authentication credentials were not provided."),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        # Получаем все миксы, которые лайкнул пользователь
        liked_mixes = MixLikes.objects.filter(user=user).values_list('mix', flat=True)
        queryset = Mixes.objects.filter(id__in=liked_mixes)

        # Пагинация
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        # Сериализация данных
        serializer = MixesSerializer(
            page if page is not None else queryset,
            many=True,
            context={'request': request}
        )

        # Возвращаем пагинированный или полный ответ
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список лайкнутых миксов успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserFavoritedMixesView(APIView):
    """
    Получение списка миксов, которые добавлены в избранное текущим пользователем.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Миксы'],
        operation_summary="Получение списка избранных миксов текущим пользователем",
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
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                         example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test Mix"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                  example="A delicious mix of flavors."),
                                    "banner": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                             example="http://localhost:8000/media/mix_banner.jpg"),
                                    "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-10-01T12:00:00Z"),
                                    "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=42),
                                    "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                    "categories": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Fruit"),
                                            }
                                        )
                                    ),
                                    "goods": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_UUID,
                                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Apple"),
                                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="Reyes-Ryan"),
                                                "image": openapi.Schema(type=openapi.TYPE_STRING,
                                                                        format=openapi.FORMAT_URI,
                                                                        example="http://localhost:8000/media/tobacco_image.jpg"),
                                                "weight": openapi.Schema(type=openapi.TYPE_INTEGER, example=50),
                                            }
                                        )
                                    ),
                                    "bowl": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                            "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="A bowl with a single hole in the center."),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/bowl_image.jpg"),
                                        }
                                    ),
                                    "author": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="123e4567-e89b-12d3-a456-426614174000"),
                                            "username": openapi.Schema(type=openapi.TYPE_STRING, example="testuser"),
                                            "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
                                            "avatar": openapi.Schema(type=openapi.TYPE_STRING,
                                                                     format=openapi.FORMAT_URI,
                                                                     example="http://localhost:8000/media/avatar.jpg"),
                                        }
                                    ),
                                }
                            )
                        )
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Authentication credentials were not provided."),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        # Получаем все миксы, которые добавлены в избранное пользователем
        favorited_mixes = MixFavorites.objects.filter(user=user).values_list('mix', flat=True)
        queryset = Mixes.objects.filter(id__in=favorited_mixes)

        # Пагинация
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        # Сериализация данных
        serializer = MixesSerializer(
            page if page is not None else queryset,
            many=True,
            context={'request': request}
        )

        # Возвращаем пагинированный или полный ответ
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Список избранных миксов успешно получен",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
