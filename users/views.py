import sentry_sdk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.CustomLimitOffsetPagination import CustomLimitOffsetPagination
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserCreateSerializer, CustomUserUpdateSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserListAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Получение списка пользователей",
        operation_description=(
                "Возвращает список всех пользователей с возможностью фильтрации по email.\n\n"
                "- Поддерживает фильтрацию через поле `email`.\n"
                "- Поддерживает пагинацию через параметры `limit` и `offset`.\n"
                "- Требуется аутентификация администратора через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Фильтр по email (необязательно)",
                                        example="user@example.com"),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER,
                                        description="Максимальное количество записей на странице", example=10),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER, description="Смещение для пагинации", example=0),
            }
        ),
        responses={
            200: openapi.Response(
                description="Список пользователей успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Список пользователей успешно получен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "results": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                                 example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                            "email": openapi.Schema(type=openapi.TYPE_STRING,
                                                                    example="user@example.com"),
                                            "username": openapi.Schema(type=openapi.TYPE_STRING, example="user123"),
                                            "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="User"),
                                            "date_joined": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          format=openapi.FORMAT_DATETIME,
                                                                          example="2023-01-01T12:00:00Z"),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=25),
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
            403: openapi.Response(
                description="Доступ запрещён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуются права администратора"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request):
        queryset = CustomUser.objects.all()
        email = request.data.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        paginator = CustomLimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = CustomUserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Получение информации о пользователе по ID",
        operation_description=(
                "Возвращает детальную информацию о пользователе по его идентификатору.\n\n"
                "- Требуется передать `id` в теле запроса.\n"
                "- Доступно только администратору или авторизованному пользователю.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                     description="ID пользователя", example="82b74c74-2399-405a-83af-26761b6fcd5b"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Информация о пользователе успешно получена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Информация о пользователе успешно получена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="user@example.com"),
                                "username": openapi.Schema(type=openapi.TYPE_STRING, example="user123"),
                                "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="User"),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-01-01T12:00:00Z"),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'id' обязательно"),
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
            403: openapi.Response(
                description="Доступ запрещён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Доступ запрещён"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Пользователь с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        user = get_object_or_404(CustomUser, id=user_id)
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"error": "Permission denied"}, status=403)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Создание нового пользователя",
        operation_description=(
                "Создаёт нового пользователя с указанными данными.\n\n"
                "- Требуются поля `email`, `username` и `password`.\n"
                "- Доступно всем пользователям, не требует аутентификации."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password'],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email пользователя",
                                        example="newuser@example.com"),
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя",
                                           example="newuser123"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Пароль пользователя",
                                           example="securepassword123"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Пользователь успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Пользователь успешно создан"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                          example="User created successfully"),
                                "user_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                          example="0084f87f-75df-42ff-965f-69eb711a66ff"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании пользователя",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при создании пользователя"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=True,
                            example={"email": ["This field is required"]}
                        )
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": str(user.id)}, status=201)
        return Response(serializer.errors, status=400)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Полное обновление данных пользователя",
        operation_description=(
                "Обновляет все поля пользователя по его ID.\n\n"
                "- Требуется передать `id` и обновляемые данные.\n"
                "- Доступно администратору или самому пользователю.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                     description="ID пользователя", example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email пользователя",
                                        example="updateduser@example.com"),
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя",
                                           example="updateduser123"),
                "nickname": openapi.Schema(type=openapi.TYPE_STRING, description="Никнейм пользователя",
                                           example="UpdatedUser"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Данные пользователя успешно обновлены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Данные пользователя успешно обновлены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="updateduser@example.com"),
                                "username": openapi.Schema(type=openapi.TYPE_STRING, example="updateduser123"),
                                "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="UpdatedUser"),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-01-01T12:00:00Z"),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Ошибка при обновлении пользователя"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"email": ["This field is required"]})
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
            403: openapi.Response(
                description="Доступ запрещён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Доступ запрещён"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Пользователь с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def put(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        user = get_object_or_404(CustomUser, id=user_id)
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"error": "Permission denied"}, status=403)
        serializer = CustomUserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserPartialUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Частичное обновление данных пользователя",
        operation_description=(
                "Обновляет указанные поля пользователя по его ID.\n\n"
                "- Требуется передать `id` и обновляемые данные.\n"
                "- Доступно администратору или самому пользователю.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                     description="ID пользователя", example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email пользователя",
                                        example="updateduser@example.com"),
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя",
                                           example="updateduser123"),
                "nickname": openapi.Schema(type=openapi.TYPE_STRING, description="Никнейм пользователя",
                                           example="UpdatedUser"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Данные пользователя успешно обновлены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Данные пользователя успешно обновлены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="updateduser@example.com"),
                                "username": openapi.Schema(type=openapi.TYPE_STRING, example="updateduser123"),
                                "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="UpdatedUser"),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-01-01T12:00:00Z"),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Ошибка при обновлении пользователя"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT,
                                               example={"nickname": ["This field may not be blank"]})
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
            403: openapi.Response(
                description="Доступ запрещён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Доступ запрещён"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Пользователь с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def patch(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        user = get_object_or_404(CustomUser, id=user_id)
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"error": "Permission denied"}, status=403)
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Удаление пользователя",
        operation_description=(
                "Удаляет пользователя по его ID.\n\n"
                "- Требуется передать `id` в теле запроса.\n"
                "- Доступно только администратору и самому пользователю.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                     description="ID пользователя", example="82b74c74-2399-405a-83af-26761b6fcd5b"),
            }
        ),
        responses={
            204: openapi.Response(
                description="Пользователь успешно удалён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Пользователь успешно удалён"),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Поле 'id' обязательно"),
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
            403: openapi.Response(
                description="Доступ запрещён",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуются права администратора"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Пользователь с указанным ID не найден"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def delete(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=204)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    sentry_sdk.set_tag("view", "UserProfileView")

    @swagger_auto_schema(
        tags=['Пользователи'],
        operation_summary="Получение профиля текущего пользователя",
        operation_description=(
                "Возвращает данные профиля авторизованного пользователя.\n\n"
                "- Не требует параметров в теле запроса.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={}
        ),
        responses={
            200: openapi.Response(
                description="Профиль пользователя успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="Профиль пользователя успешно получен"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="82b74c74-2399-405a-83af-26761b6fcd5b"),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="user@example.com"),
                                "username": openapi.Schema(type=openapi.TYPE_STRING, example="user123"),
                                "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="User"),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                              example="2023-01-01T12:00:00Z"),
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
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Требуется аутентификация"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)  # Логируем ошибку
