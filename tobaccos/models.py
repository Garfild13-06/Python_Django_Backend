import uuid
from manufacturers.models import Manufacturers
from django.db import models

# Create your models here.
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
        db_table='app_tobaccos'

    def __str__(self):
        return self.taste