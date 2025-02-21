from django.db import models
import uuid
from bowls.models import Bowls
from tastecategories.models import TasteCategories

from tobaccos.models import Tobaccos
from users.models import CustomUser


class MixTasteType(models.TextChoices):
    """Типы вкуса."""
    EMPTY = '-', '-'
    FRUIT = 'fruit', 'фруктовый'
    GASTRO = 'gastro', 'гастро'
    SWEET = 'sweet', 'сладкий'
    GRASS = 'grass', 'травяной'
    FRESH = 'fresh', 'свежий'


class Mixes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Название", max_length=200, null=False)
    description = models.TextField("Описание", default=None, blank=True)
    banner = models.ImageField(default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(TasteCategories, related_name='mixes')

    tasteType = models.CharField(
        verbose_name="Тип вкуса",
        max_length=10,
        choices=MixTasteType.choices,
        default=MixTasteType.EMPTY
    )
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='mixes')

    def total_likes(self):
        """Метод, который вернёт общее количество лайков для микса"""
        return self.likes.count()

    def add_like(self, user):
        """Метод `add_like` добавляет лайк к миксу от указанного пользователя.
        Если лайк уже существует, метод вернет существующий объект `Like`"""
        like, created = MixLikes.objects.get_or_create(user=user, mix=self)
        return like

    def remove_like(self, user):
        """Метод `remove_like` удаляет лайк от пользователя к миксу"""
        try:
            like = MixLikes.objects.get(user=user, mix=self)
            like.delete()
        except MixLikes.DoesNotExist:
            pass

    def add_to_favorites(self, user):
        """Метод `add_to_favorites` принимает пользователя (`user`), который добавляет микс в избранное.
        Метод создает запись в модели `Favorite`, связывая пользователя и микс.
        Если запись уже существует, метод возвращает существующий объект `Favorite`."""
        favorite, created = MixFavorites.objects.get_or_create(user=user, mix=self)
        return favorite

    def remove_from_favorites(self, user):
        """Метод `remove_from_favorites` удаляет запись из модели `Favorite`,
        связанную с указанным пользователем и миксом"""
        try:
            favorite = MixFavorites.objects.get(user=user, mix=self)
            favorite.delete()
        except MixFavorites.DoesNotExist:
            pass

    class Meta:
        verbose_name = "Микс"
        verbose_name_plural = "Миксы"
        db_table = "app_mixes"

    def __str__(self):
        return self.name


class MixTobacco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mix = models.ForeignKey(
        Mixes,
        on_delete=models.CASCADE,
        verbose_name="Микс",
        related_name="compares")

    tobacco = models.ForeignKey(
        Tobaccos,
        on_delete=models.CASCADE,
        verbose_name="Табак",
        related_name="compares")

    weight = models.IntegerField("%")

    class Meta:
        db_table = "app_mixtobacco"


class MixBowl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mix = models.OneToOneField(
        "Mixes",
        on_delete=models.CASCADE,
        verbose_name="Микс",
        related_name="bowl"
    )
    bowl = models.ForeignKey(
        Bowls,  # Ссылка на модель Bowls
        on_delete=models.CASCADE,
        verbose_name="Чаша",
        related_name="mixes"
    )

    class Meta:
        verbose_name = "Чаша микса"
        verbose_name_plural = "Чаши миксов"
        db_table = "app_mixbowl"


class MixLikes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mix = models.ForeignKey(
        Mixes,
        on_delete=models.CASCADE,
        verbose_name="Микс",
        related_name="likes",
        to_field="id")

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="likes",
        to_field="id")

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лайк микса"
        verbose_name_plural = "Лайки миксов"
        db_table = "app_mixlikes"


class MixFavorites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mix = models.ForeignKey(
        Mixes,
        on_delete=models.CASCADE,
        verbose_name="Микс",
        related_name="favorites",
        to_field="id")

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorites",
        to_field="id")

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранный микс"
        verbose_name_plural = "Избранные миксы"
        db_table = "app_mixfavorites"
