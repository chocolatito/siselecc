#from django.utils import timezone

from ..gest_preparacion.models import Eleccion


def set_status(id, status):
    """
    https://mattsegal.dev/simple-scheduled-tasks.html
    """
    eleccion = Eleccion.objects.get(id=id)
    eleccion.eleccion_estatus = status
    eleccion.save()
