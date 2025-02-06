# Сериализатор для чаш
from rest_framework import serializers

from bowls.models import Bowls


class BowlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bowls
        fields = ['id', 'type', 'description', 'howTo', 'image']  # Поля, которые будут включены в сериализатор
