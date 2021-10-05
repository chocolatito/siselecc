import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ..BaseModel import Base
from ..gest_cargo.models import Cargo
from ..gest_elector.models import Elector
# from ..gest_usuario.models import Cuenta
# Create your models here.
from ..utils import vname_f

ETAPAS = [(0, "PREPARACIÓN"), (1, "PROGRAMADA"), (2, "LISTA"),
          (3, "EN CURSO"), (4, "CERRADA"),
          (5, "CONTEO INICIADO"), (6, "CONTEO FINALIZADO")]


class Eleccion(Base):
    titulo = models.CharField('Titulo', max_length=100)
    fecha = models.DateField('Fecha de realización', default=datetime.date.today)
    hora_inicio = models.TimeField('Hora de inicio', blank=True, null=True)
    hora_fin = models.TimeField('Hora de cierre', blank=True, null=True)
    etapa = models.IntegerField('Etapa de elección', choices=ETAPAS, default=0)
    slug = models.SlugField(max_length=50, unique=True)
    # Relationships
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha', 'titulo']
        verbose_name = 'Eleccion'
        verbose_name_plural = 'Elecciones'

    def get_absolute_url(self):
        return reverse('gest_preparacion:detalle', args=[str(self.id)])
    # _

    def get_ini_conteo_url(self):
        return reverse('gest_cifrado:ini-conteo', args=[str(self.id)])

    def get_cifrado_url(self):
        return reverse('gest_cifrado:ini-publica-i', args=[str(self.id)])

    def get_descifrado_url(self):
        return reverse('gest_cifrado:ini-privada-i', args=[str(self.id)])

    def get_proxima_url(self):
        return reverse('bienvenida:proxima', args=[str(self.id)])

    def get_resultado_url(self):
        return reverse('bienvenida:resultado', args=[str(self.id)])

    # ____________________________________________________________________________________
    def get_field_values(self):
        return [self.titulo,
                self.fecha.strftime('%d-%m-%Y'),
                self.get_strftime(),
                self.get_etapa_display()]

    def get_field_values_bienvenida(self):
        return [self.titulo,
                self.fecha.strftime('%d-%m-%Y'), ]

    def get_strftime(self):
        if self.etapa:
            return f'{self.hora_inicio.strftime("%H:%M")} - {self.hora_fin.strftime("%H:%M")}'
        else:
            return '00:00 - 00:00'

    def get_progr_inicio(self):
        return datetime.datetime.strptime(f'{self.fecha.strftime("%Y %m %d")} {self.hora_inicio.strftime("%H %M")}', "%Y %m %d %H %M")

    def get_progr_fin(self):
        return datetime.datetime.strptime(f'{self.fecha.strftime("%Y %m %d")} {self.hora_fin.strftime("%H %M")}', "%Y %m %d %H %M")
    # ____________________________________________________________________________________

    def get_detali_info(self):
        """ [(verbose_name, value_field), ]"""
        return [(vname_f(self._meta, 'titulo'), self.titulo),
                (vname_f(self._meta, 'fecha'), self.fecha),
                ('Horarios de Inicio-Fin', self.get_strftime()),
                (vname_f(self._meta, 'etapa'), self.get_etapa_display()),
                ('Cargo', self.cargo)]

    def __str__(self):
        return "{} - {}".format(self.fecha, self.titulo)

    def es_proxima(self):
        return self.fecha >= datetime.datetime.now().date()

    def es_programable(self):
        if self.es_proxima():
            fecha_anterior = self.fecha - datetime.timedelta(days=1)
            if fecha_anterior <= datetime.datetime.now().date():
                # La Eleccion puede programarce
                if self.padron.vacio():
                    # El Padron no posee electores
                    return 2
                else:
                    if self.mesa.estado_mesa in [1, 2]:
                        if self.candidatos().count() >= 2:
                            # La eleccion es programable
                            return 5
                        else:
                            # Se necesitan mas de un candidato postulado
                            return 4
                    else:
                        # La Mesa no posee Autoridad
                        return 3
            else:
                # Falta mas de 24hs para poder programar la eleccion
                return 1
        else:
            return False
    # ____________________________________________________________________________________
    # Querysets basados en relaciones

    def candidatos(self):
        return self.candidato_set.filter(estado_postulacion=True)

    def n_candidatos(self):
        return self.candidatos().count()

    def get_claves_candidatos(self):
        cuenta = self.mesa.cuenta
        return self.clave_set.exclude(cuenta=cuenta)

    def get_clave_autoridad(self):
        cuenta = self.mesa.cuenta
        return self.clave_set.get(cuenta=cuenta)

    def get_n_staff(self):
        cuenta = self.mesa.cuenta
        return int(self.clave_set.get(cuenta=cuenta).n)


# _Candidato
class Candidato(Base):
    estado_postulacion = models.BooleanField(verbose_name="Estado de postulación",
                                             default=True)
    # Relationships REVISAR
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    elector = models.ForeignKey(Elector, on_delete=models.CASCADE)

    class Meta:
        ordering = ['estado_postulacion', ]
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

    def get_absolute_url(self):
        # return reverse('padron:edit-padron', args=[str(self.id)])
        pass

    def get_field_values(self):
        # return []
        pass

    def get_field_values_candidato(self):
        return [self.elector.dni, self.elector.nombres, self.elector.apellidos, ]

    def full_name(self):
        return f'{self.elector.apellidos}, {self.elector.nombres}'

    def __str__(self):
        return f'{self.elector.dni} / {self.elector.nombres} {self.elector.apellidos}'


# https://docs.djangoproject.com/en/3.1/topics/db/models/#extra-fields-on-many-to-many-relationships

ESTADO_PADRON = [(0, "ABIERTO"), (1, "PREPARADO"), (2, "EN OPERACIÓN"), (3, "CERRADO"), ]


# _Padron
class Padron(Base):
    estado_padron = models.IntegerField('Etapa de padrón', choices=ESTADO_PADRON, default=0)
    # slug = models.SlugField(unique=True)
    # Relationships
    eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE)
    electores = models.ManyToManyField(Elector, through='PadronElector')

    class Meta:
        ordering = ['estado_padron']
        verbose_name = "Padron"
        verbose_name_plural = "Padrones"

    def get_field_values(self):
        # return [self.title, self.slug]
        pass

    def get_absolute_url(self):
        return reverse('gest_preparacion:adm-padron', args=[self.id])

    # ___________________________________
    # PADRON VACIO
    def vacio(self):
        if self.padronelector_set.all():
            return False
        else:
            return True

    def __str__(self):
        return f'{self.id}-{self.eleccion}'


ESTADO_PADRONELECTOR = [(0, "AUSENTE"), (1, "AUTORIZADO"), (2, "RETIRADO"), ]


# _PadronElector
class PadronElector(Base):
    padron = models.ForeignKey(Padron, on_delete=models.CASCADE)
    elector = models.ForeignKey(Elector, on_delete=models.CASCADE)
    estado_padronelector = models.IntegerField(verbose_name="Estado padron-elecctor",
                                               choices=ESTADO_PADRONELECTOR,
                                               default=0)
    hora_votacion = models.DateTimeField(verbose_name="Hora de votación",
                                         null=True, blank=True)
    codigo_votacion = models.UUIDField(verbose_name="Código de votación",
                                       null=True, blank=True)

    def get_field_values(self):
        return [self.elector.dni, self.elector.apellidos, self.elector.nombres,
                self.get_estado_padronelector_display()]

    class Meta:
        unique_together = [['padron', 'elector']]


ESTADO_MESA = [(0, "CREADA"), (1, "CON AUTORIDAD"),
               (2, "PREPARADA"),
               (3, "INICIADA"), (4, "LISTA"), (5, "OPERATIVA"),
               (6, "CERRADA"), ]


# _Mesa
class Mesa(Base):
    estado_mesa = models.IntegerField('Estado de mesa', choices=ESTADO_MESA, default=0)
    # slug = models.SlugField(unique=True)
    # Relationships
    eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['estado_mesa']
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def get_absolute_url(self):
        return reverse('gest_preparacion:adm-mesa', args=[self.id])

# _Iniciada mesa
    def get_ini_url(self):
        return reverse('gest_votacion:ini-mesa', args=[self.id])

# _Mesa iniciada
    def get_mesa_ini_url(self):
        return reverse('gest_votacion:mesa-ini', args=[self.id])

# _Mesa operativa
    def get_absolute_url_mesa_ope(self):
        return reverse('gest_votacion:mesa-ope', args=[self.id])

    def get_detali_info(self):
        """[(verbose_name, value_field), ]"""
        return [(vname_f(self._meta, 'estado_mesa'), self.get_estado_mesa_display()), ]

    def __str__(self):
        return "{}".format(self.id)


# _______________________________________________________
# PRE/POST SAVE
def set_slug_Eleccion(sender, instance, *args, **kwargs):
    if instance.id and instance.titulo and instance.fecha and not instance.slug:
        instance.slug = slugify(
            f'{instance.fecha}__{instance.id}_{instance.titulo}')
        instance.save()


post_save.connect(set_slug_Eleccion, sender=Eleccion)
