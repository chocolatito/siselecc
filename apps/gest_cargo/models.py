from django.db import models
from django.urls import reverse

from ..BaseModel import Base
# Create your models here.


class Cargo(Base):
    nombre = models.CharField(verbose_name='Nombre del Cargo',
                              max_length=100, unique=True)
    descripcion = models.TextField(verbose_name='Descripción')
    editable = models.BooleanField(verbose_name='Editable', default=True)

    class Meta:
        ordering = ['nombre', ]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def get_absolute_url(self):
        return reverse('gest_cargo:detalle', args=[str(self.id)])

    def get_field_values(self):
        return [self.nombre, self.descripcion, self.editable]

    def get_detali_info(self):
        return [(self._meta.get_field('nombre').verbose_name.title(), self.nombre),
                (self._meta.get_field('descripcion').verbose_name.title(), self.descripcion),
                (self._meta.get_field('editable').verbose_name.title(), self.editable), ]

    def elecciones(self):
        """retorna las elecciones en las que se elige representante para el cargo"""
        return self.eleccion_set.all()

    def __str__(self):
        return "{}".format(self.nombre)
