from django.db.models import Q
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
    if eleccion.etapa == 0:
        eleccion.mesa.estado_mesa = 2
        eleccion.mesa.save()
        eleccion.padron.estado_padron = 1
        eleccion.padron.save()
        eleccion.etapa = 1
        eleccion.save()
        generar_boletas(eleccion, get_postulados(eleccion))
    return eleccion

# ________________________________
