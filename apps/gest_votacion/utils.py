import hashlib
from datetime import datetime
from random import shuffle
from django.core.exceptions import ObjectDoesNotExist
#
from phe import paillier
#
from .models import Urna, Voto
from ..gest_cifrado.models import Clave
from ..utils import get_user


def get_urna(mesa):
    try:
        return mesa.urna
    except ObjectDoesNotExist:
        mesa.estado_mesa = 3
        mesa.save()
        hash = mesa.eleccion.get_clave_autoridad().hash
        return Urna.objects.create(codigo_inicio=hash, mesa=mesa)


# _______________________________________________________________________________________
def actualizar_urna(urna, estado):
    urna.estado_urna = estado
    # urna.hora_inicio = HORA ACTUAL
    urna.save()
    mesa = urna.mesa
    mesa.estado_mesa = 4
    mesa.save()
    return True


def inciar_urna(ingreso, color, urna):
    codigo = hashlib.md5(f'{ingreso}+{color}'.encode()).hexdigest()
    if urna.codigo_inicio == codigo:
        return actualizar_urna(urna, 1)
    else:
        # CODIGO INCORRECTO
        return False
# ________________________________________________________________________________________


def autorizar_elector(pad_elec, urna):
    pad_elec.estado_padronelector = 1
    pad_elec.save()
    urna.estado_urna = 2
    urna.save()


def retirar_elector(pad_elec, urna):
    pad_elec.estado_padronelector = 2
    pad_elec.save()
    urna.estado_urna = 1
    urna.save()


# ________________________________________________________________________________________
def es_autoridad(mesa, user):
    """Utilizado en las vistas: IniMesa, MesaIni, MesaOpe y AutorizarElector"""
    return mesa.cuenta == get_user(user)


# _
def get_padronelector(mesa):
    """Utilizado en la vista MesaOpe"""
    return mesa.eleccion.padron.padronelector_set.all()


# _
def get_boleta(urna, id_boleta):
    return urna.mesa.eleccion.boleta_set.get(id=id_boleta)


def get_boletas(mesa):
    lista_boletas = list(mesa.eleccion.boleta_set.all())
    shuffle(lista_boletas)
    return lista_boletas

# _


def cifrar(vector, eleccion, autoridad):
    # Eleccion deberia definir un metodo que excluya la clave de staff
    clave = Clave.objects.filter(eleccion=eleccion).exclude(
        cuenta=autoridad).order_by('?').first()
    publica = paillier.PaillierPublicKey(int(clave.n))
    # tipo_vector = type(vector)
    vector_cifrado = [str(publica.encrypt(x).ciphertext()) for x in vector]
    return vector_cifrado, clave


def emitir_voto(boleta, urna):
    now = datetime.now()
    vector_candidato = boleta.vector_candidato['vector_candidato']
    eleccion = boleta.eleccion
    autoridad = urna.mesa.cuenta
    vector_cifrado, clave = cifrar(vector_candidato, eleccion, autoridad)
    Voto.objects.create(vector_cifrado=vector_cifrado,
                        hash_voto=now.strftime("%H:%M:%S"),
                        urna=urna, clave=clave)
