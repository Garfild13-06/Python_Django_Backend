from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from tobaccos.models import Tobaccos
from tobaccos.serializers import TobaccosSerializer, TobaccosDetailSerializer, TobaccosListSerializer
from utils.CustomLimitOffsetPagination import CustomLimitOffsetPagination


class TobaccoListAPIView(APIView):
    """
    Обработка POST-запроса для получения списка табаков.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Табаки'],  # Группа операций в Swagger
        operation_summary="Получение списка табаков",  # Краткое описание
        operation_description=(
                "Возвращает список всех доступных табаков.\n\n"
                "- Поддерживает поиск по полям `taste` и `description` через параметр `search`.\n\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`."
        ),
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Текст для поиска",
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
                description="Список табаков успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Список табаков успешно получен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                         example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                    "taste": openapi.Schema(type=openapi.TYPE_STRING, example="rate"),
                                    "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                            example="http://localhost:8000/media/Tobacco_UIQs82L.jpg"),
                                    "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, example="Reyes-Ryan"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                  example="Put not tonight cup road have hold year..."),
                                    "params": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, example="9"),
                                            "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                 example="low"),
                                            "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                example="middle"),
                                        }
                                    ),
                                }
                            )
                        ),
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
        queryset = Tobaccos.objects.all()

        # Если передан параметр 'search', фильтруем QuerySet
        if search_query:
            queryset = queryset.filter(
                Q(taste__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Пагинация
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        # Сериализация данных
        serializer = TobaccosListSerializer(
            page if page is not None else queryset,
            many=True,
            context={'request': request}  # Передаем request для формирования абсолютных ссылок
        )

        # Возвращаем пагинированный или полный ответ
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response(serializer.data, status=200)


class TobaccoDetailAPIView(APIView):
    """
    Обработка POST-запроса для получения деталей табака по его ID, переданному в теле запроса.
    """
    permission_classes = [AllowAny]  # Разрешаем доступ всем
    authentication_classes = []  # Аутентификация не требуется

    @swagger_auto_schema(
        tags=['Табаки'],  # Группа операций в Swagger
        operation_summary="Получение информации о табаке по ID",
        operation_description=(
                "Возвращает детальную информацию о табаке по его уникальному идентификатору.\n\n"
                "- Требуется передать `id` в теле запроса."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
            },
            required=["id"],
        ),
        responses={
            200: openapi.Response(
                description="Информация о табаке успешно получена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Информация о табаке успешно получена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="rate"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/Tobacco_UIQs82L.jpg"),
                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, example="Reyes-Ryan"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Put not tonight cup road have hold year..."),
                                "params": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, example="9"),
                                        "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING, example="low"),
                                        "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, example="middle"),
                                    }
                                ),
                            }
                        ),
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
                                                  example="Некорректные данные в теле запроса"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Табак с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        # Извлекаем id из тела запроса
        tobacco_id = request.data.get("id")
        if not tobacco_id:
            return Response({
                "status": "bad",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Поле 'id' обязательно для заполнения",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Получаем объект табака или возвращаем 404, если он не существует
        instance = get_object_or_404(Tobaccos, pk=tobacco_id)
        serializer = TobaccosDetailSerializer(instance, context={'request': request})

        return Response({
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Информация о табаке успешно получена",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class TobaccoCreateAPIView(APIView):
    """
    Создание нового табака.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Табаки'],  # Группа операций в Swagger
        operation_summary="Создание нового табака",  # Краткое описание
        operation_description=(
                "Создает новый табак.\n\n"
                "**Требует аутентификации по токену.**\n"
                "- Пользователь должен быть авторизован через JWT.\n"
                "- В теле запроса необходимо передать данные табака."
        ),
        request_body=openapi.Schema(  # Описание тела запроса
            type=openapi.TYPE_OBJECT,
            required=['taste', 'manufacturer', 'image'],  # Обязательные поля
            properties={
                'taste': openapi.Schema(type=openapi.TYPE_STRING, description="Вкус табака"),
                'manufacturer': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                               description="ID производителя"),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description="Изображение табака"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="Описание табака (необязательно)"),
                'tobacco_strength': openapi.Schema(type=openapi.TYPE_STRING, enum=['1', '2', '3'],
                                                   description="Крепость табака"),
                'tobacco_resistance': openapi.Schema(type=openapi.TYPE_STRING, enum=['low', 'medium', 'high'],
                                                     description="Теплостойкость табака"),
                'tobacco_smokiness': openapi.Schema(type=openapi.TYPE_STRING, enum=['low', 'medium', 'high'],
                                                    description="Дымность табака"),
            }
        ),
        responses={  # Возможные ответы
            201: openapi.Response(
                description="Табак успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Табак успешно создан"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="0084f87f-75df-42ff-965f-69eb711a66ff"),
                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Fruity Mix"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/Tobacco_lapD25A.jpg"),
                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                               example="123e4567-e89b-12d3-a456-426614174000"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="A fruity and refreshing tobacco blend."),
                                "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, example="7"),
                                "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING, example="middle"),
                                "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, example="high"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании табака",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при создании табака"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=True,
                            example={
                                "taste": ["This field is required."],
                                "manufacturer": ["Invalid UUID."]
                            }
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
                                                  example="Authentication credentials were not provided.")
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = TobaccosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Табак успешно создан",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при создании табака",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TobaccoUpdateAPIView(APIView):
    """
    Полное обновление данных о табаке.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Табаки'],
        operation_summary="Полное обновление данных о табаке по ID",
        operation_description=(
                "Обновляет все поля табака.\n\n"
                "- Требует аутентификации по токену."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="New Taste"),
                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                               example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение табака (опционально)"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Updated description of the tobacco."),
                "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, enum=["1", "2", "3", "4", "5"],
                                                   example="3"),
                "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING, enum=["low", "medium", "high"],
                                                     example="medium"),
                "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, enum=["low", "medium", "high"],
                                                    example="high"),
            },
            required=["taste", "manufacturer"],
        ),
        responses={
            200: openapi.Response(
                description="Табак успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Табак успешно обновлен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="New Taste"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/Tobacco_UIQs82L.jpg"),
                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, example="Reyes-Ryan"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Updated description of the tobacco."),
                                "params": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, example="3"),
                                        "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING,
                                                                             example="medium"),
                                        "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, example="high"),
                                    }
                                ),
                            }
                        ),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении табака"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Необходима авторизация"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Табак с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Tobaccos, pk=pk)
        serializer = TobaccosSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Табак успешно обновлен",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении табака",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TobaccoPartialUpdateAPIView(APIView):
    """
    Частичное обновление данных о табаке.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Табаки'],
        operation_summary="Частичное обновление данных о табаке по ID",
        operation_description=(
                "Обновляет только указанные поля табака.\n\n"
                "- Требует аутентификации по токену."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Taste"),
                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                               example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение табака (опционально)"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Partially updated description."),
                "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, enum=["1", "2", "3", "4", "5"],
                                                   example="4"),
                "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING, enum=["low", "medium", "high"],
                                                     example="high"),
                "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, enum=["low", "medium", "high"],
                                                    example="medium"),
            },
            required=[],
        ),
        responses={
            200: openapi.Response(
                description="Табак успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Табак успешно обновлен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "taste": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Taste"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/Tobacco_UIQs82L.jpg"),
                                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING, example="Reyes-Ryan"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Partially updated description."),
                                "params": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "tobacco_strength": openapi.Schema(type=openapi.TYPE_STRING, example="4"),
                                        "tobacco_resistance": openapi.Schema(type=openapi.TYPE_STRING, example="high"),
                                        "tobacco_smokiness": openapi.Schema(type=openapi.TYPE_STRING, example="medium"),
                                    }
                                ),
                            }
                        ),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении табака"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Необходима авторизация"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Табак с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def patch(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Tobaccos, pk=pk)
        serializer = TobaccosSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "code": status.HTTP_200_OK,
                "message": "Табак успешно обновлен",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "bad",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Ошибка при обновлении табака",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TobaccoDestroyAPIView(APIView):
    """
    Удаление табака.
    """
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию
    authentication_classes = [JWTAuthentication]  # Используем JWT-аутентификацию

    @swagger_auto_schema(
        tags=['Табаки'],
        operation_summary="Удаление табака по ID",
        operation_description=(
                "Удаляет табак.\n\n"
                "- Требует аутентификации по токену."
        ),
        responses={
            204: openapi.Response(
                description="Табак успешно удален",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Табак успешно удален"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Необходима авторизация"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Табак с указанным ID не существует"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Tobaccos, pk=pk)
        instance.delete()
        return Response({
            "status": "ok",
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Табак успешно удален",
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)