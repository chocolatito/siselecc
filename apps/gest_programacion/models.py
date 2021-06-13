from django.db import models

from ..BaseModel import Base
from ..gest_preparacion.models import Eleccion, Candidato

# Create your models here.
# https://docs.djangoproject.com/en/3.1/ref/databases/#sqlite-json1


class Boleta(Base):
    n = models.IntegerField(verbose_name='N', default=0)
    indice = models.IntegerField(verbose_name='Indice', default=0)
    vector_candidato = models.JSONField(verbose_name="Vector candidato")
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE,
                                     null=True, blank=True)

    class Meta:
        ordering = ['indice', ]
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"

    def get_absolute_url(self):
        # return reverse('eleccion:cargo-detail', args=[str(self.id)])
        pass

    def get_info_alternativa(self):
        if self.candidato:
            return self.candidato.__str__()
        else:
            return "Voto en Blanco"

    def __str__(self):
        return "{} de {} - Vector={}".format(self.indice, self.n, self.vector_candidato)
