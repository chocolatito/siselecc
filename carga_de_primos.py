import os
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siselecc.local")
django.setup()

from apps.gest_cifrado.models import SecuenciaPrimo

def get_rutas():
    # ruta_base = os.path.dirname(__file__)
    ruta_base = os.getcwd()
    return [ruta_base+'/300txt/'+f'{(x*240100)}.txt' for x in range(300)]


"""
def escribir_objeto(indice, ruta):
    print(indice)
    f = open(ruta, 'r')
    SecuenciaPrimo.objects.create(indice=indice,
                                  secuencia={
                                      'indice': indice,
                                      'secuencia': re.findall('\d+', f.read())})
    f.close()
"""


def main():
    rutas = get_rutas()
    [print(x) for x in rutas]
    print(f'Los filas de la tabla son::: {SecuenciaPrimo.objects.all().count()}')
    # [escribir_objeto((x*240100), rutas[x]) for x in range(300)]
