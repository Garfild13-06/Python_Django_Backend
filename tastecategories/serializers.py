from rest_framework import serializers
from tastecategories.models import TasteCategories

# Сериализатор для категорий вкусов
class TasteCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteCategories
        fields = ['id', 'name']