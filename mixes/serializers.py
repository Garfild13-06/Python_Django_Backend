from rest_framework import serializers

from utils.to_camel_case import to_camel_case
from .models import Mixes, MixTobacco, MixBowl
from tobaccos.serializers import TobaccosSerializer, TobaccosListSerializer, TobaccosDetailSerializer
from bowls.serializers import BowlsSerializer
from tastecategories.serializers import TasteCategoriesSerializer
from users.serializers import CustomUserSerializer


class MixTobaccoSerializer(serializers.ModelSerializer):
    tobacco = TobaccosListSerializer(read_only=True)
    weight = serializers.IntegerField()

    class Meta:
        model = MixTobacco
        fields = ['tobacco', 'weight']


class MixTobaccoListSerializer(serializers.ModelSerializer):
    tobacco = TobaccosListSerializer(read_only=True)
    weight = serializers.IntegerField()

    class Meta:
        model = MixTobacco
        fields = ['tobacco', 'weight']


class MixTobaccoDetailSerializer(serializers.ModelSerializer):
    tobacco = TobaccosDetailSerializer(read_only=True)
    weight = serializers.IntegerField()

    class Meta:
        model = MixTobacco
        fields = ['tobacco', 'weight']


class MixBowlSerializer(serializers.ModelSerializer):
    bowl = BowlsSerializer(read_only=True)

    class Meta:
        model = MixBowl
        fields = ['bowl']

    def to_representation(self, instance):
        # Получаем данные чаши из поля bowl
        bowl_data = self.fields['bowl'].to_representation(instance.bowl)
        return bowl_data


class MixesListSerializer(serializers.ModelSerializer):
    categories = TasteCategoriesSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    goods = MixTobaccoListSerializer(source='compares', many=True, read_only=True)

    class Meta:
        model = Mixes
        fields = [
            'id',
            'name',
            'description',
            'banner',
            'created',
            'likes_count',
            'is_liked',
            'is_favorited',
            'categories',
            'goods',
            'author'
        ]

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        camel_case_representation = {}
        for key, value in representation.items():
            camel_case_key = to_camel_case(key)
            camel_case_representation[camel_case_key] = value
        return camel_case_representation


class MixesDetailSerializer(serializers.ModelSerializer):
    categories = TasteCategoriesSerializer(many=True, read_only=True)
    goods = MixTobaccoDetailSerializer(source='compares', many=True, read_only=True)  # Табаки
    bowl = MixBowlSerializer(read_only=True)  # Чаша через MixBowl
    author = CustomUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Mixes
        fields = [
            'id', 'name', 'description', 'banner', 'created',
            'likes_count', 'is_liked', 'is_favorited',
            'categories', 'goods', 'bowl', 'author'
        ]

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        camel_case_representation = {}
        for key, value in representation.items():
            camel_case_key = to_camel_case(key)
            camel_case_representation[camel_case_key] = value
        return camel_case_representation


class MixesSerializer(serializers.ModelSerializer):
    categories = TasteCategoriesSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    goods = MixTobaccoSerializer(source='compares', many=True, read_only=True)
    bowl = BowlsSerializer(source='bowl.bowl', read_only=True)

    class Meta:
        model = Mixes
        fields = [
            'id', 'name', 'description', 'banner', 'created',
            'likes_count', 'is_liked', 'is_favorited',
            'categories', 'goods', 'bowl', 'author'
        ]

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        camel_case_representation = {}
        for key, value in representation.items():
            camel_case_key = to_camel_case(key)
            camel_case_representation[camel_case_key] = value
        return camel_case_representation

    def validate(self, data):
        # categories через initial_data, потому что это ManyToMany
        categories = self.initial_data.get('categories')
        if categories and len(categories) != 2:
            raise serializers.ValidationError("Микс должен содержать ровно 2 категории вкусов.")
        return data
