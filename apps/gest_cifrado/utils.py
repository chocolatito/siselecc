from json import loads
from functools import reduce

from django_q.models import Schedule
from .models import SecuenciaPrimo
from .models import Clave
from ..gest_usuario.models import CuentaElector

REFERENCIA = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
              'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '10',
              'k': '11', 'l': '12', 'm': '13', 'n': '14', 'ñ': '15',
              'o': '16', 'p': '17', 'q': '18', 'r': '19', 's': '20',
              't': '21', 'u': '22', 'v': '23', 'w': '24', 'x': '25',
              'y': '26', 'z': '27',
              'A': '28', 'B': '29', 'C': '30', 'D': '31', 'E': '32',
              'F': '33', 'G': '34', 'H': '35', 'I': '36', 'J': '37',
              'K': '38', 'L': '39', 'M': '40', 'N': '41', 'Ñ': '42',
              'O': '43', 'P': '44', 'Q': '45', 'R': '46', 'S': '47',
              'T': '48', 'U': '49', 'V': '50', 'W': '51', 'X': '52',
              'Y': '53', 'Z': '54',
              '0': '55', '1': '56', '2': '57', '3': '58', '4': '59',
              '5': '60', '6': '61', '7': '62', '8': '63', '9': '64',
              '.': '65', ',': '66', '_': '67', '-': '68', '$': '69',
              '@': '70'}


# ________________________________________________________________________________________
# SecuenciaPrimo.objects.create(indice=indice, secuencia={'indice': indice, 'sec': re.findall('\d+', f.read())})
"""
import re
from os.path import dirname
from .models import SecuenciaPrimo
def get_fraccion(indice, ruta):
    print(indice)
    f = open(ruta, 'r')
    #
    f.close()


def generar_secuencias():
    ruta = dirname(__file__) + '\\total\\'
    [get_fraccion(x, ruta+f'{x}.txt') for x in range(0, 72030000, 240100)]"""
# ________________________________________________________________________________________


def verificar_user_elector(user, candidatos):
    try:
        cuentaelector = CuentaElector.objects.get(cuenta=user)
    except CuentaElector.DoesNotExist:
        cuentaelector = None
    if cuentaelector:
        return candidatos.filter(elector=cuentaelector.elector).exists()
    else:
        return False
# ________________________________________________________________________________________


def todas_las_claves(e):
    """ e: Eleccion"""
    if e.clave_set.all().count() == e.candidato_set.all().count()+1:
        e.etapa = 2
        e.save()
        # programar el inicio https://youtu.be/KXP84ijiLbg?t=880
        Schedule.objects.create(name=f'{e.id} st2: {e.get_progr_inicio()}',
                                     func='apps.gest_programacion.tasks.set_status',
                                     args=f'{e.id},{3}',
                                     schedule_type='O',
                                     repeats=1,
                                     next_run=e.get_progr_inicio()
                                )
        # programar el final
        Schedule.objects.create(name=f'{e.id} st3: {e.get_progr_fin()}',
                                     func='apps.gest_programacion.tasks.set_status',
                                     args=f'{e.id},{4}',
                                     schedule_type='O',
                                     repeats=1,
                                     next_run=e.get_progr_fin()
                                )
        return True
    else:
        return False


def calcular_indices(ingreso, segmento):
    valor = ingreso*segmento
    indice = ((valor-1) // 240100) * 240100
    indiceSec = (valor-1) % 240100
    tipo_indice = type(indice)
    if SecuenciaPrimo.objects.get(indice=indice):
        existeSecPri = True
        tipo_sec = type(loads(SecuenciaPrimo.objects.get(indice=indice).secuencia))
        tipo_secsec = type(loads(SecuenciaPrimo.objects.get(indice=indice).secuencia)['sec'])
        tipo_indiceSec = type(indiceSec)
    else:
        existeSecPri = False
    return int(SecuenciaPrimo.objects.get(indice=indice).secuencia['sec'][indiceSec])


def get_valor_clave(clave):
    return reduce(lambda x, y: x*y, [int(REFERENCIA[x]) for x in clave])


def generar_N(ingreso, segmento):
    sub_claves = (get_valor_clave(ingreso[:4]), get_valor_clave(ingreso[4:8]))
    return str(calcular_indices(sub_claves[0], segmento[0]) * calcular_indices(sub_claves[1], segmento[0]))


def generar_Cpublica(ingreso, color, cuenta, eleccion):
    n = generar_N(ingreso, color)
    Clave.objects.create(n=n, cuenta=cuenta, eleccion=eleccion)
    return todas_las_claves(eleccion)


# ________________________________________________________________________________________
def verificar_user_clave(eleccion, cuenta):
    if eleccion.clave_set.filter(cuenta=cuenta):
        return False
    else:
        return True
