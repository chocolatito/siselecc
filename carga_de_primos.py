import os
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siselecc.production")
django.setup()

from apps.gest_cifrado.models import SecuenciaPrimo

def escribir_objeto(indice):
    print(indice)
    f = open(f'/home/debpps/secuencia_num_primos/300txt/{(indice)}.txt', 'r')
    SecuenciaPrimo.objects.create(indice=indice,
                                  secuencia={
                                      'indice': indice,
                                      'secuencia': re.findall('\d+', f.read())})
    f.close()


def main():
    [escribir_objeto((x*240100)) for x in range(300)]
    print(f'Los filas de la tabla son::: {SecuenciaPrimo.objects.all().count()}')
