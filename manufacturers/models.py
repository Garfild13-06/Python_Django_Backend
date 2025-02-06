from bowls.models import *


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
        db_table='app_manufacturers'

    def __str__(self):
        return self.name
