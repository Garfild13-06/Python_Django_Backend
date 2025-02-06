from rest_framework import serializers

from manufacturers.models import Manufacturers


# Сериализатор для производителей
class ManufacturersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturers
        fields = ['id', 'name', 'description', 'image']  # Поля, которые будут включены в сериализатор
