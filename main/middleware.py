from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse

HTTP_STATUS_DESCRIPTIONS = {
    # Информационные ответы
    100: {"status": "good", "description": "Продолжай"},
    101: {"status": "good", "description": "Переключение протоколов"},
    102: {"status": "good", "description": "Обработка"},
    103: {"status": "good", "description": "Ранние подсказки"},

    # Успешные ответы
    200: {"status": "good", "description": "Успех"},
    201: {"status": "good", "description": "Создано"},
    202: {"status": "good", "description": "Принято"},
    203: {"status": "good", "description": "Информация не авторитетна"},
    204: {"status": "good", "description": "Нет содержимого"},
    205: {"status": "good", "description": "Сбросить содержимое"},
    206: {"status": "good", "description": "Частичное содержимое"},
    207: {"status": "good", "description": "Мульти-статус"},
    208: {"status": "good", "description": "Уже сообщается"},
    226: {"status": "good", "description": "Использовано"},

    # Перенаправления
    300: {"status": "good", "description": "Множественный выбор"},
    301: {"status": "good", "description": "Перемещено навсегда"},
    302: {"status": "good", "description": "Найдено"},
    303: {"status": "good", "description": "Смотри другое"},
    304: {"status": "good", "description": "Не изменялось"},
    305: {"status": "good", "description": "Использовать прокси"},
    307: {"status": "good", "description": "Временное перенаправление"},
    308: {"status": "good", "description": "Постоянное перенаправление"},

    # Клиентские ошибки
    400: {"status": "bad", "description": "Некорректный запрос"},
    401: {"status": "bad", "description": "Не авторизован"},
    403: {"status": "bad", "description": "Запрещено"},
    404: {"status": "bad", "description": "Не найдено"},
    405: {"status": "bad", "description": "Метод не поддерживается"},
    422: {"status": "bad", "description": "Необрабатываемый экземпляр"},
    429: {"status": "bad", "description": "Слишком много запросов"},

    # Ошибки сервера
    500: {"status": "bad", "description": "Внутренняя ошибка сервера"},
    501: {"status": "bad", "description": "Не реализовано"},
    503: {"status": "bad", "description": "Сервис недоступен"},
    504: {"status": "bad", "description": "Шлюз не отвечает"},
}


class ResponseMiddleware:
    """
    Middleware для унификации всех ответов API.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(f"[Middleware] Обрабатываем запрос: {request.method} {request.path}")

        if (
                request.path.startswith("/admin")
                or request.path.startswith("/swagger")
                or request.path.startswith(settings.MEDIA_URL)
                or request.path.startswith("/api/v1/auth/")
        ):
            return self.get_response(request)

        response = self.get_response(request)

        # Рендерим содержимое, если требуется
        if hasattr(response, 'render') and callable(response.render):
            try:
                response = response.render()
            except Exception as e:
                print(f"[Middleware] Ошибка рендеринга: {e}")
                return JsonResponse({
                    "status": "bad",
                    "code": 500,
                    "message": "Ошибка рендеринга ответа",
                    "data": None
                }, status=500)

        # Получаем информацию о статусе из словаря
        status_info = HTTP_STATUS_DESCRIPTIONS.get(
            response.status_code,
            {"status": "bad", "description": "Неизвестный статус"}
        )

        # Проверка наличия данных
        if hasattr(response, 'data') and isinstance(response.data, dict):
            if 200 <= response.status_code < 300:
                # Успешный ответ
                # data = response.data
                if "data" in response.data:
                    data = response.data["data"]
                else:
                    data = response.data
                errors = None
            else:
                # Ошибочный ответ
                data = None
                errors = response.data
        else:
            # Если данных нет
            data = None
            errors = None

        # Формируем единый формат ответа
        response_data = {
            "status": status_info["status"],
            "code": response.status_code,
            "message": status_info["description"],
            "data": data,
            "errors": errors,
        }

        # Всегда возвращаем JsonResponse
        return JsonResponse(response_data, status=response.status_code)
