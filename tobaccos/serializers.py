from rest_framework import serializers

from tobaccos.models import Tobaccos


class TobaccosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tobaccos
        fields = ['id', 'taste', 'manufacturer', 'image', 'description']  # Поля для отображения товаров


class TobaccosListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)

    class Meta:
        model = Tobaccos
        fields = ['id', 'taste', 'image', 'manufacturer', 'tobacco_strength', 'tobacco_resistance', 'tobacco_smokiness',
                  'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['params'] = {
            'tobacco_strength': representation.pop('tobacco_strength'),
            'tobacco_resistance': representation.pop('tobacco_resistance'),
            'tobacco_smokiness': representation.pop('tobacco_smokiness')
        }
        return representation


class TobaccosDetailSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)

    class Meta:
        model = Tobaccos
        fields = ['id', 'taste', 'image', 'manufacturer', 'description', 'tobacco_strength', 'tobacco_resistance',
                  'tobacco_smokiness']
