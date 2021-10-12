from ..BaseModel import Base
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from ..utils import vname_f

# Create your models here.


mim_max = [MinValueValidator(9999999, message='Numero menor a un 10 millones'),
           MaxValueValidator(99999999, message='Numero mayor o igual a un 100 millones')]


class Elector(Base):
    dni = models.PositiveIntegerField(verbose_name="DNI", validators=mim_max, unique=True)
    nombres = models.CharField(verbose_name="Nombre/s",
                               max_length=100, null=False, blank=False)
    apellidos = models.CharField(verbose_name="Apellido/s",
                                 max_length=100, null=False, blank=False)
    correo = models.EmailField(verbose_name='Correo Electrónico', unique=True)
    cuenta_u = models.BooleanField(verbose_name="Cuenta de usuario", default=False,
                                   null=False, blank=False)

    class Meta:
        ordering = ['nombres', 'apellidos', 'dni']
        verbose_name = "Elector"
        verbose_name_plural = "Electores"

    def get_absolute_url(self):
        return reverse('gest_elector:detalle', args=[str(self.id)])

    def get_field_values(self):
        return [self.dni, self.nombres, self.apellidos, self.cuenta_u]

    # __
    def get_detali_info(self):
        """ [(verbose_name, value_field), ]"""
        return [(vname_f(self._meta, 'dni'), self.dni),
                (vname_f(self._meta, 'nombres'), self.nombres),
                (vname_f(self._meta, 'apellidos'), self.apellidos),
                (vname_f(self._meta, 'correo'), self.correo), ]
        # (vname_f(self._meta, 'cuenta_u'), self.cuenta_u),

    # __

    def get_field_values_cuenta(self):
        return [self.dni, self.nombres, self.apellidos, ]

    def get_field_values_padron(self):
        return [self.dni, self.nombres, self.apellidos, ]

    def get_field_values_candidato(self):
        return [self.dni, self.nombres, self.apellidos, ]

    def get_field_values_votacion(self):
        # return [self.dni, self.names, self.surnames]
        pass

    def full_names(self):
        return f'{self.apellidos}, {self.nombres}'

    def __str__(self):
        return f'{self.dni} - {self.nombres} {self.apellidos}'
