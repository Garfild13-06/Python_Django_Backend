from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from manufacturers.models import Manufacturers
from bowls.models import Bowls
from tobaccos.models import Tobaccos
from .serializers import MiniManufacturerSerializer, MiniBowlSerializer, MiniTobaccoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SelectionOptionsAPIView(APIView):
    """
    Получение списка производителей и чаш.

    ---
    **POST** `/api/v1/selection/options/`

    Возвращает два массива:
    - `manufacturers` — список производителей (id и name)
    - `bowls` — список чаш (id и type)

    - Не требует аутентификации.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["Вспомогательные выборки"],
        operation_summary="Получение списка производителей и чаш",
        operation_description="Возвращает два массива: список производителей и список чаш. Аутентификация не требуется.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "manufacturers": [
                            {"id": "uuid", "name": "DarkSide"},
                            {"id": "uuid", "name": "MustHave"},
                        ],
                        "bowls": [
                            {"id": "uuid", "type": "Phunnel"},
                            {"id": "uuid", "type": "Killer"},
                        ]
                    }
                }
            )
        }
    )
    def post(self, request):
        manufacturers = Manufacturers.objects.all()
        bowls = Bowls.objects.all()
        return Response({
            "manufacturers": MiniManufacturerSerializer(manufacturers, many=True).data,
            "bowls": MiniBowlSerializer(bowls, many=True).data,
        }, status=status.HTTP_200_OK)


class TobaccosByManufacturerAPIView(APIView):
    """
    Получение списка табаков по ID производителя.

    ---
    **POST** `/api/v1/selection/tobaccos-by-manufacturer/`

    Принимает:
    - `manufacturer_id` (UUID)

    Возвращает:
    - массив табаков (`id`, `taste`)

    - Не требует аутентификации.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["Вспомогательные выборки"],
        operation_summary="Получение табаков по ID производителя",
        operation_description="Принимает `manufacturer_id` в теле запроса и возвращает список табаков. Аутентификация не требуется.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["manufacturer_id"],
            properties={
                "manufacturer_id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID,
                                                  description="ID производителя")
            }
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "tobaccos": [
                            {"id": "uuid", "taste": "Grape Mint"},
                            {"id": "uuid", "taste": "Mango Ice"},
                        ]
                    }
                }
            )
        }
    )
    def post(self, request):
        manufacturer_id = request.data.get("manufacturer_id")
        if not manufacturer_id:
            return Response({"error": "Поле 'manufacturer_id' обязательно."}, status=status.HTTP_400_BAD_REQUEST)

        tobaccos = Tobaccos.objects.filter(manufacturer_id=manufacturer_id)
        return Response({
            "tobaccos": MiniTobaccoSerializer(tobaccos, many=True).data
        }, status=status.HTTP_200_OK)
