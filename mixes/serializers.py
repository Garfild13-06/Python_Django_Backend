from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from tastecategories.serializers import TasteCategoriesSerializer
from mixes.models import MixTobacco, MixBowl, Mixes, MixLikes, MixFavorites
from users.models import CustomUser


class MixAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname', 'avatar']  # Включаем минимальные поля


class MixTobaccoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='tobacco.id')
    taste = serializers.CharField(source='tobacco.taste')
    manufacturer = serializers.CharField(source='tobacco.manufacturer')
    image = serializers.ImageField(source='tobacco.image')
    weight = serializers.IntegerField()  # Вес табака в миксе

    class Meta:
        model = MixTobacco
        fields = ['id', 'taste', 'manufacturer', 'image', 'weight']  # Отображаем табак и вес из MixTobacco


class MixBowlSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='bowl.id')
    type = serializers.CharField(source='bowl.type')
    description = serializers.CharField(source='bowl.description')
    image = serializers.ImageField(source='bowl.image')

    class Meta:
        model = MixBowl
        fields = ['id', 'type', 'description', 'image']


# Сериализатор для миксов
class MixesSerializer(serializers.ModelSerializer):
    categories = TasteCategoriesSerializer(many=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = MixAuthorSerializer(read_only=True)  # Вложенный сериализатор для автора
    goods = MixTobaccoSerializer(source='compares', many=True,
                                 read_only=True)  # Связь через поле `compares` в MixTobacco
    bowl = MixBowlSerializer(read_only=True)  # Связь с чашей

    class Meta:
        model = Mixes
        fields = ['id', 'name', 'description', 'banner', 'created', 'likes_count', 'is_liked', 'is_favorited',
                  'categories', 'goods', 'bowl', 'author']

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return MixLikes.objects.filter(mix=obj, user_id=request.user.id).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return MixFavorites.objects.filter(mix=obj, user_id=request.user.id).exists()
        return False

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user  # Назначаем автором текущего пользователя
            mix = Mixes.objects.create(**validated_data)
            return mix
        else:
            raise serializers.ValidationError("User not authenticated")