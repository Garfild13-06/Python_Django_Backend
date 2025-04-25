from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """Кастомная офсетная пагинация."""

    max_limit = 100  # Максимально допустимое количество элементов
    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = request.data.get('limit', self.default_limit)
        self.offset = request.data.get('offset', 0)

        try:
            self.limit = int(self.limit)
            self.offset = int(self.offset)
        except (ValueError, TypeError):
            return []

        if self.limit > self.max_limit:
            self.limit = self.max_limit

        self.count = queryset.count()
        self.request = request
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        next_offset = self.offset + self.limit if (self.offset + self.limit) < self.count else None
        previous_offset = self.offset - self.limit if (self.offset - self.limit) >= 0 else None

        return Response({
            "count": self.count,
            "next": next_offset,
            "previous": previous_offset,
            "results": data
        })

