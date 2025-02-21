from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """Кастомная офсетная пагинация."""

    max_limit = 100  # Максимально допустимое количество элементов
    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        # Извлекаем параметры из тела запроса (body)
        limit = request.data.get('limit')
        offset = request.data.get('offset', 0)  # По умолчанию offset = 0

        if limit is None:
            limit = self.default_limit
        try:
            self.limit = int(limit)
            self.offset = int(offset)
        except ValueError:
            return Response({
                "status": "bad",
                "code": 400,
                "message": "Некорректное значение для 'limit' или 'offset'."
            }, status=400)

        if self.limit > self.max_limit:
            return Response({
                "status": "bad",
                "code": 400,
                "message": f"Значение 'limit' не может превышать {self.max_limit}."
            }, status=400)

        self.count = queryset.count()
        self.request = request

        if self.offset >= self.count:
            return []

        return list(queryset[self.offset:self.offset + self.limit])
