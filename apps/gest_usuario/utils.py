import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import CuentaElector
from ..gest_elector.models import Elector
from siselecc.settings import (EMAIL_HOST,
                               EMAIL_PORT,
                               EMAIL_HOST_USER,
                               EMAIL_HOST_PASSWORD,)


# http://chuwiki.chuidiang.org/index.php?title=Enviar_y_leer_email_con_python_y_gmail
def send_email(username, clave, email_to):
    try:

        # Establecemos conexion con el servidor smtp de gmail
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        # Construimos el mensaje simple
        mensaje = MIMEText(f"{username}, {clave}")
        mensaje['From'] = EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Confirmar cuenta de usuario"
        # Envio del mensaje
        # mailServer.sendmail(EMAIL_HOST_USER, email_to, mensaje.as_string())
        return True
    except Exception as e:
        print(e)
        return False


# ___________________________
def get_elector_list(id_list):
    return [Elector.objects.get(id=id) for id in id_list]


def gen_cuenta_elector(usuario, elector):
    object = CuentaElector(cuenta=usuario, elector=elector)
    object.save()
    # EL PASSWORD DEBE MEJORARSE
    send_email(usuario.username, usuario.username, elector.correo)
    print(object)


def gen_cuenta(elector):
    group = Group.objects.get(name='elector')
    # EL PASSWORD DEBE MEJORARSE
    user = User.objects.create_user(str(elector.dni), elector.correo, str(elector.dni))
    user.groups.add(group)
    elector.cuenta_u = True
    elector.save()
    gen_cuenta_elector(user, elector)
    return user


def gen_cuentas_e(elector_id_list):
    """LLamado desde la CBV ElectorSinCuentaListView"""
    [gen_cuenta(elector) for elector in get_elector_list(elector_id_list)]


# ________________________
def actualizar_cuentaelector(electorcuenta):
    # incluir una bloque try
    electorcuenta.estado_confirmacion = True
    electorcuenta.confirmacion = datetime.now()
    electorcuenta.save()
