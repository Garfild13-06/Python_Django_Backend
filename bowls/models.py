# bowls/models.py
from django.db import models
import uuid


class Bowls(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField("Тип чаши", max_length=200, null=False)
    description = models.TextField("Описание", default=None, blank=True)
    howTo = models.TextField("Инструкция", default=None, blank=True)
    image = models.ImageField(default=None, blank=True)

    class Meta:
        verbose_name = "Чаша"
        verbose_name_plural = "Чаши"
        db_table='app_bowls'

    def __str__(self):
        return self.type
