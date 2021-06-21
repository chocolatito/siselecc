from django.db import models
from django.conf import settings
from ..BaseModel import Base
from ..gest_preparacion.models import Eleccion

# Create your models here.


class Clave(Base):
    hash = models.CharField(verbose_name='Hash', max_length=32)
    n = models.CharField(verbose_name='Clave pública', max_length=100, default='')
    creacion = models.DateTimeField(verbose_name='Fecha  y hora de creacón',
                                    auto_now_add=True)
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['eleccion', 'cuenta', 'creacion']
        verbose_name = "Clave"
        verbose_name_plural = "Claves"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return [self.name, self.description, self.get_editable_display()]
        pass

    def __str__(self):
        return "{} - {} de {}".format(self.n, self.eleccion, self.cuenta)


class Resultado(Base):
    final = models.BooleanField(verbose_name='Resultado final', default=False)
    parciales = models.IntegerField(verbose_name='Parciales restantes', default=0)
    vector_resultado = models.JSONField(verbose_name="Vector resultado", default={})
    creacion = models.DateTimeField(verbose_name='Fecha y hora de creacón',
                                    auto_now_add=True)
    hash_final = models.CharField(verbose_name='Hash final',
                                  max_length=100, null=True)
    eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['creacion', 'final']
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return [self.name, self.description, self.get_editable_display()]
        pass

    def __str__(self):
        return "{} de {}".format(self.vector_resultado, self.parciales)


class Parcial(Base):
    suma = models.JSONField(verbose_name="Suma parcial")
    descifrado = models.BooleanField(verbose_name='Descifrado', default=False)
    fecha_hora = models.DateTimeField(verbose_name='Fecha y hora de obtención',
                                      auto_now_add=True)
    hash_final = models.CharField(verbose_name='Hash',
                                  max_length=100, null=True)
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE)
    clave = models.ForeignKey(Clave, on_delete=models.CASCADE)

    class Meta:
        ordering = ['descifrado']
        verbose_name = "Parcial"
        verbose_name_plural = "Parciales"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return [self.name, self.description, self.get_editable_display()]
        pass

    def __str__(self):
        return "{} de {}".format(self.suma, self.descifrado)


class SecuenciaPrimo(Base):
    indice = models.IntegerField(verbose_name='indice de la secuencia')
    secuencia = models.JSONField(verbose_name="Secuencia de 1250 numeros primos")

    class Meta:
        ordering = ['indice', ]
        verbose_name = "SecuenciaPrimo"
        verbose_name_plural = "Secuencia de Primos"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return [self.name, self.description, self.get_editable_display()]
        pass

    def __str__(self):
        return f'{self.indice}'
