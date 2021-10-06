from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView

from .utils import gen_cuentas_e
from .models import CuentaElector
from ..gest_elector.models import Elector

# Create your views here.


class LoginFormView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                print(f'Usuario: {request.user}')
                print(f"URL: {redirect('bienvenida:bienvenida')} ...")
                return redirect('bienvenida:bienvenida')
        print(f'Usuario: {request.user}')
        print(f"URL: {redirect('bienvenida:bienvenida')} ...")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar Sesión"
        return context


def logout_view(request):
    logout(request)
    return redirect('bienvenida:bienvenida')

# _______________________


# ____________________________________________
# _Elector
# decorators = [login_required, group_required('staff',)]
decorators = [login_required(login_url='gest_usuario:login'), ]


# path: gen-cue-elector/ | gen-cu-elector
@ method_decorator(decorators, name='dispatch')
class ElectorSinCuentaListView(ListView):
    model = Elector
    template_name = 'gest_usuario/elector_sin_cuenta_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """"""
        return self.model.objects.filter(cuenta_u=False)

    def post(self, request, *args, **kwargs):
        if request.POST.getlist('elector_enabled'):
            gen_cuentas_e(request.POST.getlist('elector_enabled'))
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Electores sin Cuenta'
        context['page_title_heading'] = 'Elector sin Cuenta'
        context['message_no_queryset'] = 'No hay electores registrados sin cuenta'
        context['thead_values'] = ['DNI', 'Nombre/s', 'Apellido/s', ]
        context['url_listado_E'] = 'gest_elector:listado'
        context['url_listado_CE'] = 'gest_usuario:cuenta-elector'
        # context['url_detalle'] = 'gest_elector:detalle'
        # context['url_actualizar'] = 'gest_elector:actualizar'
        return context


# path: cuenta-elector/ | cuenta-elector
@ method_decorator(decorators, name='dispatch')
class CuentaElectorListView(ListView):
    model = CuentaElector
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    template_name = 'gest_usuario/cuenta_elector_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cuenta de Electores'
        context['page_title_heading'] = 'Cuentas de Elector'
        context['message_no_queryset'] = 'No hay electores registrados con cuenta'
        context['thead_values'] = ['DNI', 'Correo', 'Cuenta', 'Confirmación', 'Elector', ]
        context['url_listado_E'] = 'gest_elector:listado'
        context['url_listado_CE'] = 'gest_elector:listado'
        # context['url_detalle'] = 'gest_elector:detalle'
        # context['url_actualizar'] = 'gest_elector:actualizar'
        return context
