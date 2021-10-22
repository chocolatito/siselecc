import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siselecc.local")
django.setup()

from django_q.models import Schedule
from django.db.models import Q
from apps.gest_preparacion.models import Eleccion


def main():
    today = date.today()
    proximas = Eleccion.objects.filter(Q(etapa=1) and Q(fecha__lt=today))
    if proximas:
        proximas.update(etapa=7)
        
