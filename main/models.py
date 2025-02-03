from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Поле Email должно быть заполнено'))
        if not username:
            raise ValueError(_('Поле Username должно быть заполнено'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    email = models.EmailField(unique=True, verbose_name="Email")
    username = models.CharField(max_length=150, unique=True, verbose_name="Username")
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name="Аватар")
    nickname = models.CharField(max_length=100, null=True, blank=True, verbose_name="Никнейм")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = f'User-{str(self.id)[-6:]}'
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class TobaccoLeaf(models.TextChoices):
    """Варианты типов листа."""
    EMPTY = "-", ""
    VIRGINIA = 'virginia', 'virginia'
    BURLEY = 'burley', 'burley'
    ORIENTAL = 'oriental', 'oriental'


class TobaccoResistance(models.TextChoices):
    """Варианты теплостойкости."""
    EMPTY = '-', ''
    LOW = 'low', 'низкая'
    MIDDLE = 'middle', 'средняя'
    HIGH = 'high', 'высокая'


class TobaccoSmokiness(models.TextChoices):
    """Варианты теплостойкости."""
    EMPTY = '-', ''
    LOW = 'low', 'низкая'
    MIDDLE = 'middle', 'средняя'
    HIGH = 'high', 'высокая'


class TobaccoStrength(models.TextChoices):
    """Варианты крепости."""
    ZERO = '0', '0'
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'
    SIX = '6', '6'
    SEVEN = '7', '7'
    EIGHT = '8', '8'
    NINE = '9', '9'
    TEN = '10', '10'


class Manufacturers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        "Название",
        max_length=200,
        null=False)

    description = models.TextField(
        verbose_name="Описание производителя",
        default=None,
        blank=True)

    image = models.ImageField(
        default=None,
        blank=True)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Tobaccos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    manufacturer = models.ForeignKey(
        Manufacturers,
        on_delete=models.CASCADE,
        related_name="Tobacco",
        verbose_name="Производитель",
        null=False
    )

    taste = models.CharField(
        "Вкус",
        max_length=200,
        default=None,
        blank=True)

    image = models.ImageField(default=None, blank=True)

    # tobacco_leaf = models.CharField(
    #     verbose_name="Тип листа",
    #     max_length=15,
    #     choices=TobaccoLeaf.choices,
    #     default=TobaccoLeaf.EMPTY
    # )

    tobacco_strength = models.CharField(
        verbose_name="Крепость",
        max_length=2,
        choices=TobaccoStrength.choices,
        default=TobaccoStrength.ZERO
    )

    tobacco_resistance = models.CharField(
        verbose_name="Теплостойкость",
        max_length=15,
        choices=TobaccoResistance.choices,
        default=TobaccoResistance.EMPTY
    )
    tobacco_smokiness = models.CharField(
        verbose_name="Дымность",
        max_length=15,
        choices=TobaccoSmokiness.choices,
        default=TobaccoSmokiness.EMPTY
    )

    description = models.TextField(
        default=None,
        blank=True,
        verbose_name="Описание ингредиента")

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Табак"
        verbose_name_plural = "Табаки"

    def __str__(self):
        return self.taste


class TasteCategories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=200, null=False)

    class Meta:
        verbose_name = "Категория вкуса"
        verbose_name_plural = "Категории вкусов"

    def __str__(self):
        return self.name


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


class Bowls(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField("Тип чаши", max_length=200, null=False)
    description = models.TextField("Описание", default=None, blank=True)
    howTo = models.TextField("Инструкция", default=None, blank=True)
    image = models.ImageField(default=None, blank=True)

    class Meta:
        verbose_name = "Чаша"
        verbose_name_plural = "Чаши"

    def __str__(self):
        return self.type

class MixBowl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mix = models.OneToOneField(
        "Mixes",
        on_delete=models.CASCADE,
        verbose_name="Микс",
        related_name="bowl"
    )
    bowl = models.ForeignKey(
        "Bowls",
        on_delete=models.CASCADE,
        verbose_name="Чаша",
        related_name="mixes"
    )

    class Meta:
        verbose_name = "Чаша микса"
        verbose_name_plural = "Чаши миксов"


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
