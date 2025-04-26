from rest_framework import serializers
from manufacturers.models import Manufacturers
from bowls.models import Bowls
from tobaccos.models import Tobaccos


class MiniManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturers
        fields = ['id', 'name']


class MiniBowlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bowls
        fields = ['id', 'type']  # type вместо name


class MiniTobaccoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tobaccos
        fields = ['id', 'taste']
