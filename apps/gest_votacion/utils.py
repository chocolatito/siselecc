from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
#
from phe import paillier
#
from .models import Urna, Voto
from ..utils import get_user
from ..gest_cifrado.models import Clave


def get_urna(mesa):
    try:
        return mesa.urna
    except ObjectDoesNotExist:
        mesa.estado_mesa = 3
        mesa.save()
        return Urna.objects.create(codigo_inicio='123456789', mesa=mesa)


# ________________________________________________________________________________________

def actualizar_urna(urna, estado):
    urna.estado_urna = estado
    urna.save()
    mesa = urna.mesa
    mesa.estado_mesa = 4
    mesa.save()
    return urna


def inciar_urna(codigo):
    try:
        print('\nSe actualiza la urna\n')
        return actualizar_urna(Urna.objects.get(codigo_inicio=codigo), 1)
    except ObjectDoesNotExist:
        print('\nCODIGO INCORRECTO\n')
        return None
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
    return mesa.cuenta == get_user(user.username)


# _
def get_padronelector(mesa):
    """Utilizado en la vista MesaOpe"""
    return mesa.eleccion.padron.padronelector_set.all()


# _
def get_boleta(urna, id_boleta):
    return urna.mesa.eleccion.boleta_set.get(id=id_boleta)


# _
def cifrar(vector, eleccion):
    clave = Clave.objects.filter(eleccion=eleccion).order_by('?').first()
    publica = paillier.PaillierPublicKey(int(clave.n))
    tipo_vector = type(vector)
    vector_cifrado = [publica.encrypt(x) for x in vector]
    return vector_cifrado


def emitir_voto(boleta, urna):
    now = datetime.now()
    vector_cifrado = cifrar(boleta.vector_candidato['vector_candidato'], boleta.eleccion)
    Voto.objects.create(vector_cifrado=vector_cifrado,
                        hash_voto=now.strftime("%H:%M:%S"),
                        urna=urna)
