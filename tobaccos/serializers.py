from rest_framework import serializers
from tobaccos.models import Tobaccos


class TobaccosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tobaccos
        fields = ['id', 'taste', 'manufacturer', 'image', 'description']  # Поля для отображения товаров


class TobaccosListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    image = serializers.SerializerMethodField()  # Используем SerializerMethodField для формирования абсолютного URL

    class Meta:
        model = Tobaccos
        fields = [
            'id', 'taste', 'image', 'manufacturer', 'description',
            'tobacco_strength', 'tobacco_resistance', 'tobacco_smokiness'
        ]

    def get_image(self, obj):
        """Формирует абсолютный URL для изображения."""
        if obj.image:
            request = self.context.get('request')  # Получаем объект запроса из контекста
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None  # Если изображения нет, возвращаем None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Группируем параметры в поле "params"
        representation['params'] = {
            'tobacco_strength': representation.pop('tobacco_strength'),
            'tobacco_resistance': representation.pop('tobacco_resistance'),
            'tobacco_smokiness': representation.pop('tobacco_smokiness')
        }
        return representation


class TobaccosDetailSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    image = serializers.SerializerMethodField()  # Используем SerializerMethodField для формирования абсолютного URL

    class Meta:
        model = Tobaccos
        fields = [
            'id',
            'taste',
            'image',
            'manufacturer',
            'description',
            'tobacco_strength',
            'tobacco_resistance',
            'tobacco_smokiness'
        ]

    def get_image(self, obj):
        """
        Возвращает полный URL изображения.
        """
        if obj.image:
            request = self.context.get('request')  # Получаем объект запроса из контекста
            if request:
                return request.build_absolute_uri(obj.image.url)  # Формируем полный URL
        return None  # Если изображение отсутствует, возвращаем None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Группируем параметры в поле "params"
        representation['params'] = {
            'tobacco_strength': representation.pop('tobacco_strength'),
            'tobacco_resistance': representation.pop('tobacco_resistance'),
            'tobacco_smokiness': representation.pop('tobacco_smokiness')
        }
        return representation
