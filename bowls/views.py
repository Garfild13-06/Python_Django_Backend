from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import Bowls
from .serializers import BowlsSerializer


class BowlsListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Получение списка чаш",
        operation_description=(
                "Возвращает список всех доступных чаш.\n\n"
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
                description="Список чаш успешно получен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Список чаш успешно получен"),
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
                                            "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                            "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                                          example="Керамическая чаша для кальяна"),
                                            "howTo": openapi.Schema(type=openapi.TYPE_STRING,
                                                                    example="Уложить табак рыхло"),
                                            "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                                    example="http://localhost:8000/media/bowls/phunnel.jpg"),
                                        }
                                    )
                                ),
                                "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
                                "next": openapi.Schema(type=openapi.TYPE_STRING,
                                                       example="http://localhost:8000/api/v1/bowls/list/?limit=10&offset=10"),
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
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Получение информации о чаше по ID",
        operation_description=(
                "Возвращает детальную информацию о чаше по её уникальному идентификатору.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Доступно всем пользователям без аутентификации."
        ),
        responses={
            200: openapi.Response(
                description="Детали чаши успешно получены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Детали чаши успешно получены"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Керамическая чаша для кальяна"),
                                "howTo": openapi.Schema(type=openapi.TYPE_STRING, example="Уложить табак рыхло"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/bowls/phunnel.jpg"),
                            }
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Чаша не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Создание новой чаши",
        operation_description=(
                "Создаёт новую чашу с указанными данными.\n\n"
                "- Требуются поля `type`, `description`, `howTo`, `image` (опционально).\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['type'],
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип чаши", example="Phunnel"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание чаши",
                                              example="Керамическая чаша"),
                "howTo": openapi.Schema(type=openapi.TYPE_STRING, description="Инструкция по использованию",
                                        example="Уложить табак рыхло"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение чаши (опционально)"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Чаша успешно создана",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша успешно создана"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "type": openapi.Schema(type=openapi.TYPE_STRING, example="Phunnel"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Керамическая чаша"),
                                "howTo": openapi.Schema(type=openapi.TYPE_STRING, example="Уложить табак рыхло"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/bowls/phunnel.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при создании чаши",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при создании чаши"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"type": ["This field is required"]})
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Полное обновление данных о чаше",
        operation_description=(
                "Обновляет все поля чаши по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['type'],
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип чаши", example="Updated Phunnel"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание чаши",
                                              example="Обновлённая керамическая чаша"),
                "howTo": openapi.Schema(type=openapi.TYPE_STRING, description="Инструкция по использованию",
                                        example="Уложить табак плотно"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение чаши (опционально)"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Чаша успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша успешно обновлена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "type": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Phunnel"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING,
                                                              example="Обновлённая керамическая чаша"),
                                "howTo": openapi.Schema(type=openapi.TYPE_STRING, example="Уложить табак плотно"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/bowls/updated_phunnel.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении чаши",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении чаши"),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, example={"type": ["This field is required"]})
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
                description="Чаша не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Частичное обновление данных о чаше",
        operation_description=(
                "Обновляет указанные поля чаши по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип чаши", example="Updated Phunnel"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание чаши",
                                              example="Обновлённое описание"),
                "howTo": openapi.Schema(type=openapi.TYPE_STRING, description="Инструкция по использованию",
                                        example="Уложить табак плотно"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, description="Изображение чаши (опционально)"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Чаша успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша успешно обновлена"),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                     example="123e4567-e89b-12d3-a456-426614174000"),
                                "type": openapi.Schema(type=openapi.TYPE_STRING, example="Updated Phunnel"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, example="Обновлённое описание"),
                                "howTo": openapi.Schema(type=openapi.TYPE_STRING, example="Уложить табак плотно"),
                                "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        example="http://localhost:8000/media/bowls/updated_phunnel.jpg"),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка при обновлении чаши",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Ошибка при обновлении чаши"),
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
                description="Чаша не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['Чаши'],
        operation_summary="Удаление чаши",
        operation_description=(
                "Удаляет чашу по её ID.\n\n"
                "- Требуется передать `pk` в URL.\n"
                "- Требуется аутентификация через JWT."
        ),
        responses={
            204: openapi.Response(
                description="Чаша успешно удалена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="ok"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=204),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша успешно удалена"),
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
                description="Чаша не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="bad"),
                        "code": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Чаша с указанным ID не найдена"),
                        "data": openapi.Schema(type=openapi.TYPE_STRING, example="null"),
                    }
                )
            )
        }
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
