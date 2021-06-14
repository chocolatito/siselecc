from django.db.models import Q
##
from django_q.models import Schedule
##
from .models import Boleta
# from ..gest_preparacion.models import Padron, Mesa, Candidato


def crear_boleta(n, indice, vector, eleccion, candidato):
    Boleta.objects.create(n=n, indice=indice,
                          vector_candidato={'vector_candidato': vector},
                          eleccion=eleccion, candidato=candidato)


def generar_vector(n):
    parciales = [i*'0'+'1'+(n-i)*'0' for i in range(n+1)]
    return [[int(x) for x in cadena] for cadena in parciales]


def get_postulados(eleccion):
    return eleccion.candidato_set.filter(Q(eleccion=eleccion)
                                         and Q(estado_postulacion=True))


def generar_boletas(eleccion, candidatos):
    n = candidatos.all().count()
    vectores = generar_vector(n)
    Boleta.objects.create(n=n, indice=0,
                          vector_candidato={'vector_candidato': vectores[0]},
                          eleccion=eleccion)
    [crear_boleta(n, i, vectores[i], eleccion, candidatos[i-1]) for i in range(1, n+1, 1)]


def actualizar_etapa(eleccion):
    """ Función llamada en la vista AdmProgramacion"""
    # DEBERIA LLAMARSE actualizar_programacion
    if eleccion.etapa == 0:
        eleccion.mesa.estado_mesa = 2
        eleccion.mesa.save()
        eleccion.padron.estado_padron = 1
        eleccion.padron.save()
        eleccion.etapa = 1
        eleccion.save()
        generar_boletas(eleccion, get_postulados(eleccion))
    # programar el inicio
    Schedule.objects.create(name=f'{eleccion.id} st2: {eleccion.get_progr_inicio()}',
                                 func='apps.gest_programacion.tasks.set_status',
                                 args=f'{eleccion.id},{3}',
                                 schedule_type='O',
                                 repeats=1,
                                 next_run=eleccion.get_progr_inicio()
                            )
    # programar el final
    Schedule.objects.create(name=f'{eleccion.id} st3: {eleccion.get_progr_fin()}',
                                 func='apps.gest_programacion.tasks.set_status',
                                 args=f'{eleccion.id},{4}',
                                 schedule_type='O',
                                 repeats=1,
                                 next_run=eleccion.get_progr_fin()
                            )
    return eleccion

# ________________________________
