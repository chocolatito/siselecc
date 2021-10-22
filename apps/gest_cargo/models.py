from django.db import models
from django.urls import reverse
from ..utils import vname_f
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


    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Cargo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gest_cargo:detalle', args=[str(self.id)])

    def get_field_values(self):
        return [self.nombre, self.descripcion, self.editable]

    def get_detali_info(self):
        if self.editable:
            editable = 'Es editable'
        else:
            editable = 'No se puede editar'
        return [(vname_f(self._meta, 'nombre'), self.nombre),
                (vname_f(self._meta, 'descripcion'), self.descripcion),
                (vname_f(self._meta, 'editable'), editable), ]

    def elecciones(self):
        """retorna las elecciones en las que se elige representante para el cargo"""
        return self.eleccion_set.all()

    def __str__(self):
        return "{}".format(self.nombre)
