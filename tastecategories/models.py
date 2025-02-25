from django.db import models

# Create your models here.
from django.db import models
import uuid


class TasteCategories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=200, null=False)

    class Meta:
        verbose_name = "Категория вкуса"
        verbose_name_plural = "Категории вкусов"
        db_table = "app_tastecategories"

    def __str__(self):
        return self.name
