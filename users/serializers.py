from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from djoser.serializers import SetPasswordSerializer

from users.models import CustomUser


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
    avatar = serializers.SerializerMethodField()  # Используем SerializerMethodField для формирования абсолютного URL

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'nickname', 'avatar', 'date_joined')

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')  # Получаем объект запроса из контекста
            if request:
                return request.build_absolute_uri(obj.avatar.url)  # Формируем полный URL
        return None  # Если изображение отсутствует, возвращаем None


# Сериализатор для обновления пользователя
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()  # Используем SerializerMethodField для формирования абсолютного URL

    class Meta:
        model = CustomUser
        fields = (
            'nickname', 'avatar', 'username')  # Поля, которые будут включены в сериализатор
        read_only_fields = ('email',)  # Поле email будет только для чтения, его нельзя изменять

    def validate_nickname(self, value):
        if CustomUser.objects.filter(nickname=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Этот никнейм уже занят.")
        return value

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')  # Получаем объект запроса из контекста
            if request:
                return request.build_absolute_uri(obj.avatar.url)  # Формируем полный URL
        return None  # Если изображение отсутствует, возвращаем None


# Сериализатор для изменения пароля
class CustomSetPasswordSerializer(SetPasswordSerializer):
    new_password = serializers.CharField(write_only=True, required=True)  # Поле для нового пароля, только для записи

    def validate_new_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")  # Проверка, чтобы пароль не был пустым
        validate_password(value)
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['params'] = {
            'tobacco_strength': representation.pop('tobacco_strength'),
            'tobacco_resistance': representation.pop('tobacco_resistance'),
            'tobacco_smokiness': representation.pop('tobacco_smokiness')
        }
        return representation
