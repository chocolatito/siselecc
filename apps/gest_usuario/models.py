from django.db import models
# https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
from django.conf import settings
from ..BaseModel import Base
from ..gest_elector.models import Elector
# Create your models here.
# https://docs.djangoproject.com/en/3.1/topics/db/models/#extra-fields-on-many-to-many-relationships

CUENTA_TIPO = [(0, "STAFF"), (1, "ELECTOR")]


class Cuenta(Base):
    tipo = models.IntegerField(verbose_name='Tipo', choices=CUENTA_TIPO, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario",
                             on_delete=models.CASCADE)

    class Meta:
        # se puede ordenar por atributos de user?
        ordering = ['tipo']
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        # deberia devolver la cuenta de usuario
        return "{} - {}".format(self.user.username, self.tipo)


class CuentaElector(Base):
    creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    confirmacion = models.DateTimeField(verbose_name="Fecha de confirmación",
                                        null=True, blank=True)
    estado_confirmacion = models.BooleanField(verbose_name="Estado de confirmación",
                                              default=False)
    cuenta = models.OneToOneField(settings.AUTH_USER_MODEL,
                                  verbose_name="Cuenta", on_delete=models.CASCADE)
    elector = models.OneToOneField(Elector,
                                   verbose_name="Elector", on_delete=models.CASCADE)

    class Meta:
        # se puede ordenar por atributos de user?
        ordering = ['creacion']
        verbose_name = "CuentaElector"
        verbose_name_plural = "CuentasElector"

    def get_field_values_cuenta(self):
        return [self.elector.dni,
                self.elector.correo,
                self.cuenta,
                self.estado_confirmacion, ]

    def __str__(self):
        # deberia devolver la cuenta de usuario
        return "{}".format(self.cuenta.username)
        # return "{}".format(self.cuenta.user.username)
