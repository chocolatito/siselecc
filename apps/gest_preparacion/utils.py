from django.db.models import Q
from django.contrib.auth.models import User
from .models import Eleccion, Padron, Mesa, Candidato

from ..gest_elector.models import Elector
from ..gest_usuario.models import CuentaElector


def get_elector_exclude_candidato(excluidos, field='id'):
    if excluidos:
        lista_electores = Elector.objects.filter(
            Q(active=True) and Q(cuenta_u=True)).exclude(
                Q(id__in=excluidos.values_list(field, flat=True)))
        return [e for e in lista_electores if CuentaElector.objects.get(
            elector=e).estado_confirmacion == True]
    else:
        lista_electores = Elector.objects.filter(Q(active=True) and Q(cuenta_u=True))
        return [e for e in lista_electores if CuentaElector.objects.get(
            elector=e).estado_confirmacion == True]
        # return Elector.objects.filter(Q(active=True) & Q(cuenta_u=True))


def get_elector_exclude_padron(excluidos, field='id'):
    if excluidos:
        return Elector.objects.exclude(
            Q(id__in=excluidos.values_list(field, flat=True))).filter(
            Q(active=True) and Q(cuenta_u=True))
    else:
        permitidos = Elector.objects.filter(
            Q(active=True) and Q(cuenta_u=True) and Q(cuenta_u=True))
        finales = [p for p in permitidos if CuentaElector.objects.get(
            elector=p).estado_confirmacion == True]
        print(f'\n\n-------\n{finales}')
        return permitidos
        # return Elector.objects.filter(Q(active=True) & Q(cuenta_u=True))


def gen_padron_mesa(eleccion):
    Padron.objects.create(eleccion=eleccion)
    Mesa.objects.create(eleccion=eleccion)
    if eleccion.cargo.editable:
        eleccion.cargo.editable = False
        eleccion.cargo.save()
        return eleccion
    else:
        eleccion.cargo.editable = False
        eleccion.cargo.save()
        return eleccion

# ________________________________


def get_electores(id_list):
    return [Elector.objects.get(id=id) for id in id_list]


def admi_elector2padron(objetc, id_list, accion):
    if id_list:
        if accion == 'agregar':
            [objetc.electores.add(elector) for elector in get_electores(id_list)]
        elif accion == 'quitar':
            [objetc.electores.remove(elector) for elector in get_electores(id_list)]


def staff_list(actual):
    if actual:
        return User.objects.filter(Q(groups__name='staff') & ~Q(id=actual.id))
    else:
        return User.objects.filter(groups__name='staff')


def agregar_candidato(eleccion, elector_id):
    candidato = Candidato.objects.create(eleccion=eleccion,
                                         elector=Elector.objects.get(id=elector_id))
    print(f'El nuevo candidato:\n{candidato}\n\n')


def set_estado_postulacion(candidato):
    if candidato.estado_postulacion:
        candidato.estado_postulacion = False
    else:
        candidato.estado_postulacion = True
    candidato.save()

# ________________________________________________________________________________________


def get_eleccion(id):
    return Eleccion.objects.get(id=id)
