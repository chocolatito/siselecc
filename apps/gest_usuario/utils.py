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
def send_email(username, clave, link, email_to):
    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    # mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    mailServer.auth_plain(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    # Construimos el mensaje simple
    mensaje = MIMEText(f"Usuario::{username} Clave actual: {clave} Enlace: {link}.")
    mensaje['From'] = EMAIL_HOST_USER
    mensaje['To'] = email_to
    mensaje['Subject'] = "Confirmar cuenta de usuario"
    # Envio del mensaje
    mailServer.sendmail(EMAIL_HOST_USER, email_to, mensaje.as_string())
    return True

# ___________________________


def get_elector_list(id_list):
    return [Elector.objects.get(id=id) for id in id_list]


def gen_cuenta_elector(usuario, elector, link):
    object = CuentaElector(cuenta=usuario, elector=elector)
    object.save()
    # EL PASSWORD DEBE MEJORARSE
    return send_email(usuario.username, usuario.username, link, elector.correo)


def gen_cuenta(elector, link):
    group = Group.objects.get(name='elector')
    # EL PASSWORD DEBE MEJORARSE
    user = User.objects.create_user(str(elector.dni), elector.correo, str(elector.dni))
    user.groups.add(group)
    elector.cuenta_u = True
    elector.save()
    return gen_cuenta_elector(user, elector, link)


def gen_cuentas_e(elector_id_list, link):
    """LLamado desde la CBV ElectorSinCuentaListView"""
    if False in [gen_cuenta(elector, link) for elector in get_elector_list(elector_id_list)]:
        return False
    else:
        return True


# ________________________
def actualizar_cuentaelector(electorcuenta):
    # incluir una bloque try
    electorcuenta.estado_confirmacion = True
    electorcuenta.confirmacion = datetime.now()
    electorcuenta.save()
