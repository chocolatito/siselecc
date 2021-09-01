import hashlib

from functools import reduce
from phe import paillier
from phe.paillier import EncryptedNumber
#
from django_q.models import Schedule
from .models import SecuenciaPrimo
from .models import Clave, Resultado, Parcial
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


def es_candidato(user, candidatos):
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
    if e.clave_set.all().count() == e.candidatos().count()+1:
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
                                     func='apps.gest_programacion.tasks.carrar_votacion',
                                     args=f'{e.id}',
                                     schedule_type='O',
                                     repeats=1,
                                     next_run=e.get_progr_fin()
                                )
        return True
    else:
        return False


def get_primo(indice, sec):
    # ****************************
    # En produccion es 'secuencia'
    # En desarrollo es 'sec'
    # ****************************
    # int(SecuenciaPrimo.objects.get(indice=indice).secuencia['sec'][sec])
    return int(SecuenciaPrimo.objects.get(indice=indice).secuencia['secuencia'][sec])


def calcular_indices(ingreso, segmento):
    valor = (ingreso*segmento) - 1
    indice = (valor // 240100) * 240100
    sec = valor % 240100
    return get_primo(indice, sec)


def get_valor_clave(clave):
    return reduce(lambda x, y: x*y, [int(REFERENCIA[x]) for x in clave])


def generar_N(ingreso, segmento):
    sub_claves = (get_valor_clave(ingreso[:4]), get_valor_clave(ingreso[4:8]))
    return str(calcular_indices(sub_claves[0], segmento[0]) * calcular_indices(sub_claves[1], segmento[1]))


def generar_Cpublica(ingreso, color, cuenta, eleccion):
    n = generar_N(ingreso, color)
    hash = hashlib.md5(f'{ingreso}+{color}'.encode()).hexdigest()
    Clave.objects.create(hash=hash, n=n, cuenta=cuenta, eleccion=eleccion)
    return todas_las_claves(eleccion)


# ________________________________________________________________________________________
def verificar_user_clave(eleccion, cuenta):
    if eleccion.clave_set.filter(cuenta=cuenta):
        return False
    else:
        return True


# ________________________________________________________________________________________
def crear_resultado(eleccion):
    return Resultado.objects.create(eleccion=eleccion)


# ________________________________________________________________________________________
def actualizar_voto(voto):
    voto.estado_voto = 1
    voto.save()


def suma_individual(enc):
    # <reduce()> retora un <paillier.EncryptedNumber>
    # <paillier.EncryptedNumber.ciphertext()> retora un <int>
    # <str> retora un tipo string
    return str(reduce(lambda x, y: x+y, enc).ciphertext())


def get_EncNum(publica, vector_cifrado):
    return [EncryptedNumber(publica, v) for v in vector_cifrado]


def gen_suma_parcial(pub, votos, len_v):
    # se recupera el vector y combierte a tipo INTEGGER
    EncNums = [get_EncNum(pub, voto.get_int_vector()) for voto in votos]
    return [suma_individual([enc[i] for enc in EncNums]) for i in range(len_v)]


def generar_parcial(clave, votos, resultado):
    if votos:
        # Si existe al menos un voto cifrado con la <clave>
        suma = gen_suma_parcial(gen_publica(int(clave.n)), votos, resultado.get_len_vector())
        Parcial.objects.create(suma=suma, resultado=resultado, clave=clave)
        [actualizar_voto(v) for v in votos]


def generar_parciales(resultado, claves):
    if claves:
        [generar_parcial(clave, clave.voto_set.all(), resultado) for clave in claves]
        return True
    else:
        return False


# ________________________________________________________________________________________
def privada_iniciada(eleccion, user):
    """Retorna un <True> o <False>"""
    clave = eleccion.clave_set.get(cuenta=user)
    if clave.parcial:
        return clave.parcial.descifrado
    else:
        return False

        # ________________________________________________________________________________________


def sumar_par(alfa, beta):
    return [suma_individual([ab[i] for ab in [alfa, beta]]) for i in range(len(alfa))]


def gen_vector_resultado(publica, vector):
    return [str(v.ciphertext()) for v in get_VecEncNum(publica, vector)]


def gen_privada(public_key, p, q):
    return paillier.PaillierPrivateKey(public_key, p, q)


def gen_PQ(alfa, beta):
    # <alfa> string de 8 caracteres
    # <beta> tupla de dos enteros
    # <gamma> tupla de dos enteros
    gamma = (get_valor_clave(alfa[:4]), get_valor_clave(alfa[4:8]))
    return calcular_indices(gamma[0], beta[0]), calcular_indices(gamma[1], beta[1])


def get_VecEncNum(publica, vector):
    return [publica.encrypt(v) for v in vector]


def gen_publica(n):
    return paillier.PaillierPublicKey(n)


def desencriptar_suma(ingreso, color, cuenta, eleccion):
    """Se asume que <cuenta> corresponde a un candidato de la elección"""
    hash = hashlib.md5(f'{ingreso}+{color}'.encode()).hexdigest()
    clave = eleccion.clave_set.get(cuenta=cuenta)
    parcial = clave.parcial
    if clave.hash == hash:
        # <pub> es la clave publica
        pub = gen_publica(int(clave.n))
        p, q = gen_PQ(ingreso, color)
        # <pri> es la clave privada
        pri = gen_privada(pub, p, q)
        # retorna una lista de enteros no nulos
        suma = [pri.raw_decrypt(v) for v in parcial.int_suma()]
        parcial.descifrado = True
        parcial.save()
        return suma
    else:
        # La clave ingresada por el usuario es incorrecta
        return []


def desc_intv(privada, int_vector):
    return [privada.raw_decrypt(v) for v in int_vector]


def actualizar_resultado(ingreso, color, cuenta, eleccion):
    resultado = eleccion.resultado
    if resultado.final:
        # El ingreso corresponde al usuario tipo Staff
        hash = hashlib.md5(f'{ingreso}+{color}'.encode()).hexdigest()
        clave = eleccion.clave_set.get(cuenta=cuenta)
        if clave.hash == hash:
            # <pub_staff>: clave publica la autoridad de mesa
            # <p>,<q>: números primos
            # <pri_staff>: clave publica la autoridad de mesa
            pub_staff = gen_publica(int(clave.n))
            p, q = gen_PQ(ingreso, color)
            pri_staff = gen_privada(pub_staff, p, q)
            #
            resultado.vector_resultado = desc_intv(pri_staff, resultado.int_vector())
            resultado.save()
            #
            eleccion.etapa = 6
            eleccion.save()
            #
            return True
        else:
            return []
    suma = desencriptar_suma(ingreso, color, cuenta, eleccion)
    print(f'***********\nSUMA: {suma}')
    if suma:
        pub_staff = gen_publica(eleccion.get_n_staff())
        print(f'\nPUBLICA STAFF: {pub_staff.n}')
        if resultado.parciales:
            # r_actual = get_VecEncNum(pub_staff, resultadoint_vector))
            r_actual = get_EncNum(pub_staff, resultado.int_vector())
            r_nuevo = get_VecEncNum(pub_staff, suma)
            resultado.vector_resultado = sumar_par(r_actual, r_nuevo)
            resultado.save()
            n_parciales = resultado.parciales
            resultado.parciales = 1 + n_parciales
            resultado.save()
            if resultado.parciales == eleccion.n_candidatos():
                resultado.final = True
                resultado.save()
        else:
            print('# Se actualiza por primera ves el vector resultado')
            # Se actualiza por primera ves el vector resultado
            resultado.vector_resultado = gen_vector_resultado(pub_staff, suma)
            resultado.save()
            resultado.parciales = 1
            resultado.save()
        return True
    else:
        return False


# ________________________________________________________________________________________

# ________________________________________________________________________________________

# ________________________________________________________________________________________
