from rest_framework import serializers

from manufacturers.models import Manufacturers
from tobaccos.models import Tobaccos


class TobaccosSerializer(serializers.ModelSerializer):
    manufacturer = serializers.PrimaryKeyRelatedField(queryset=Manufacturers.objects.all())
    class Meta:
        model = Tobaccos
        fields = ['taste', 'manufacturer', 'description', 'tobacco_strength']


class TobaccosListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    image = serializers.SerializerMethodField()  # Используем SerializerMethodField для формирования абсолютного URL

    class Meta:
        model = Tobaccos
        fields = [
            'id',
            'taste',
            'image',
            'manufacturer',
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
            'strength': representation.pop('tobacco_strength'),
            'resistance': representation.pop('tobacco_resistance'),
            'smokiness': representation.pop('tobacco_smokiness')
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
            'strength': representation.pop('tobacco_strength'),
            'resistance': representation.pop('tobacco_resistance'),
            'smokiness': representation.pop('tobacco_smokiness')
        }
        return representation
