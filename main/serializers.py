from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import Tobaccos, Mixes, Manufacturers, TasteCategories, MixLikes, MixFavorites, MixTobacco, \
    MixBowl
from djoser.serializers import UserCreateSerializer, UserSerializer, SetPasswordSerializer
from .models import CustomUser

"""
Объяснение
CustomUserCreateSerializer: Сериализатор для создания пользователя, включающий поля id, email, nickname, avatar, password.
CustomUserSerializer: Сериализатор для отображения информации о пользователе, включающий поля id, email, nickname, avatar, first_name, last_name, date_joined.
CustomUserUpdateSerializer: Сериализатор для обновления пользователя, включающий поля id, email, nickname, avatar, first_name, last_name, где поле email является только для чтения.
CustomSetPasswordSerializer: Сериализатор для изменения пароля, включающий проверку, чтобы новый пароль не был пустым.
TobaccosSerializer: Сериализатор для табаков, включающий поля id, taste, image, manufacturer, description, tobacco_strength, tobacco_resistance, tobacco_smokiness. Поля tobacco_strength, tobacco_resistance, tobacco_smokiness сгруппированы в отдельный словарь params.
MixesSerializer: Сериализатор для миксов, включающий все поля модели Mixes.
BowlsSerializer: Сериализатор для чаш, включающий поля id, type, description, howTo, image.
"""


# Сериализатор для создания пользователя
class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'nickname', 'avatar', 'date_joined')

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            avatar_url = obj.avatar.url
            return request.build_absolute_uri(avatar_url)
        return ""


# Сериализатор для обновления пользователя
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'nickname', 'avatar', 'first_name', 'username')  # Поля, которые будут включены в сериализатор
        read_only_fields = ('email',)  # Поле email будет только для чтения, его нельзя изменять


# Сериализатор для изменения пароля
class CustomSetPasswordSerializer(SetPasswordSerializer):
    new_password = serializers.CharField(write_only=True, required=True)  # Поле для нового пароля, только для записи

    def validate_new_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")  # Проверка, чтобы пароль не был пустым
        validate_password(value)
        return value


# Сериализатор для табаков
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['params'] = {
            'tobacco_strength': representation.pop('tobacco_strength'),
            'tobacco_resistance': representation.pop('tobacco_resistance'),
            'tobacco_smokiness': representation.pop('tobacco_smokiness')
        }
        return representation


# Сериализатор для категорий вкусов
class TasteCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteCategories
        fields = ['id', 'name']


class MixAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname', 'avatar']  # Включаем минимальные поля


class TobaccosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tobaccos
        fields = ['id', 'taste', 'manufacturer', 'image', 'description']  # Поля для отображения товаров


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
