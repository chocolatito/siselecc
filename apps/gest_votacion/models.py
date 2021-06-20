from django.db import models
from django.urls import reverse

from ..BaseModel import Base
from ..gest_preparacion.models import Mesa
from ..gest_cifrado.models import Clave
# Create your models here.


ESTADOS_URNA = [
    (0, "CREADA"),
    (1, "LIBRE"), (2, "ESPERANDO ELECTOR"),
    (3, "EN OPERACIÓN"), (4, "EN CONFIRMACIÓN"), (5, "OPERACION COMPLETADA"),
    (6, "ELECTOR RETIRADO"),
    (7, "CERRADA"), ]


class Urna(Base):
    codigo_inicio = models.CharField('Código inicio', max_length=100)
    estado_urna = models.IntegerField('Estado de urna',
                                      choices=ESTADOS_URNA, default=0)
    creacion = models.DateTimeField(verbose_name='Fecha y hora de creacón',
                                    auto_now_add=True)
    hora_inicio = models.TimeField('Hora de inicio', blank=True, null=True)
    hora_cierre = models.TimeField('Hora de cierre', blank=True, null=True)
    # Relationships
    mesa = models.OneToOneField(Mesa, on_delete=models.CASCADE)

    class Meta:
        ordering = ['creacion', 'estado_urna']
        verbose_name = "Urna"
        verbose_name_plural = "Urnas"

# _Iniciada urna
    def get_absolute_url_ini(self):
        return reverse('gest_votacion:ini-urna')

# _Urna libre
    def get_absolute_url_urna_ope(self):
        return reverse('gest_votacion:urna-ope', args=[self.id])

# _Urna operativa
#    def get_absolute_url_urna_ope(self):
#        return reverse('gest_votacion:urna-ope', args=[self.id])

    def __str__(self):
        return "{} - {}".format(self.estado_urna, self.creacion)


PADRON_ESTADO_VOTO = [(0, "EMITIDO"), (1, "PROGRAMADA"), (2, "LISTA"),
                      (3, "EN CURSO"), (4, "CERRADA"), (5, "CONTEO INICIADO")]


class Voto(Base):
    vector_cifrado = models.JSONField(verbose_name="Vector resultado")
    hash_voto = models.CharField(verbose_name='Hash voto',
                                 max_length=100, unique=True)
    estado_voto = models.IntegerField('Estado de voto',
                                      choices=PADRON_ESTADO_VOTO, default=0)
    hora_conteo = models.DateTimeField(verbose_name='Fecha y hora de conteo',
                                       auto_now_add=True)
    urna = models.ForeignKey(Urna, on_delete=models.CASCADE)
    clave = models.ForeignKey(Clave, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['estado_voto']
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return [self.name, self.description, self.get_editable_display()]
        pass

    def __str__(self):
        return f'{self.id} - {self.vector_cifrado}'
