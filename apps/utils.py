from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


def set_active(model, id, active_value):
    set_active_field(model.objects.get(id=int(id)), active_value)


def set_active_field(object, new_value):
    if new_value:
        object.active = False
    else:
        object.active = True
    object.save()


def get_queryset_by_state(model, state):
    if state == 'activo':
        return model.objects.filter(active=True)
    elif state == 'inactivo':
        return model.objects.filter(active=False)
    else:
        return model.objects.all()


def vname_f(_meta, field):
    return _meta.get_field(field).verbose_name.title()


def login_forbidden():
    def is_loged(u):
        if not u.is_authenticated:
            return True
    return user_passes_test(is_loged, redirect_field_name='bienvenida:bienvenida')

# _______________________________


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in.
    https://stackoverflow.com/questions/36177769/django-groups-and-permissions
    https://docs.djangoproject.com/es/3.1/topics/auth/default/
    """
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, redirect_field_name='bienvenida:bienvenida')


def estado_confirmacion_required():
    """Requires user membership in at least one of the groups passed in.
    """
    def has_estado_confirmacion(u):
        if u.is_authenticated:
            try:
                if u.cuentaelector:
                    if bool(u.cuentaelector.estado_confirmacion) | u.is_superuser:
                        return True
                    else:
                        return False
            except:
                return True
        return False
    # SE DEBE PROCEDER A CONFIRMAR LA CUENTA
    return user_passes_test(has_estado_confirmacion, redirect_field_name='gest_usuario:confirmar')


def estado_confirmacion_no_required():
    """Requires user membership in at least one of the groups passed in.
    """
    def has_estado_confirmacion(u):
        if u.is_authenticated:
            if bool(u.cuentaelector.estado_confirmacion) | u.is_superuser:
                return False
            else:
                return True
        return False
    # SE DEBE PROCEDER A CONFIRMAR LA CUENTA
    return user_passes_test(has_estado_confirmacion, redirect_field_name='bienvenida:bienvenida')


# ________________________________________________________________________________________


def get_user(user):
    return User.objects.get(username=user.username)
