from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import CuentaElector
from ..gest_elector.models import Elector


def get_elector_list(id_list):
    return [Elector.objects.get(id=id) for id in id_list]


def gen_cuenta_elector(usuario, elector):
    object = CuentaElector(cuenta=usuario, elector=elector)
    object.save()
    print(object)


def gen_cuenta(elector):
    """LLamado desde la CBV ElectorSinCuentaListView"""
    group = Group.objects.get(name='elector')
    user = User.objects.create_user(str(elector.dni), elector.correo, str(elector.dni))
    user.groups.add(group)
    elector.cuenta_u = True
    elector.save()
    gen_cuenta_elector(user, elector)
    return user


def gen_cuentas_e(elector_id_list):
    [gen_cuenta(elector) for elector in get_elector_list(elector_id_list)]
