from django.db import models


class Base(models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True
