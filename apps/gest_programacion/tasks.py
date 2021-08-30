#from django.utils import timezone

from ..gest_preparacion.models import Eleccion

# Separa la actualizacion para apertura y cierre porque tambien actualiza otros objetos
# En el inicio, se tambien actualiza el padron
# En el cierre, tambien se actualiza el padron, la mesa y la urna.


def set_status(id, status):
    """
    https://mattsegal.dev/simple-scheduled-tasks.html
    """
    eleccion = Eleccion.objects.get(id=id)
    eleccion.etapa = status
    eleccion.save()
    #
    eleccion.padron.estado_padron = 2
    eleccion.save()


def carrar_votacion(id):
    """
    https://mattsegal.dev/simple-scheduled-tasks.html
    """
    eleccion = Eleccion.objects.get(id=id)
    eleccion.etapa = 4
    eleccion.save()
    # CERRADA
    eleccion.mesa.estado_mesa = 6
    eleccion.save()
    # CERRADA
    eleccion.mesa.urna.estado_urna = 7
    eleccion.save()
    # CERRADO
    eleccion.padron.estado_padron = 3
    eleccion.save()
