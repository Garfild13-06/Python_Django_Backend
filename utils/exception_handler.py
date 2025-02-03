from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        try:
            response.data = {
                "status": "bad",
                "code": response.status_code,
                "message": response.data.get("detail", "Произошла ошибка"),
                "data": None
            }
        except AttributeError:
            response.data = {
                "status": "bad",
                "code": response.status_code,
                "message": "Произошла ошибка",
                "data": None
            }
    else:
        response = Response({
            "status": "bad",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Внутренняя ошибка сервера",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
