from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView


from .forms import ClaveForm
from .utils import gen_cuentas_e, actualizar_cuentaelector
from .models import CuentaElector
from ..utils import group_required, get_user, estado_confirmacion_no_required
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
decorators = [login_required(login_url='gest_usuario:login'), group_required('staff'), ]
decorators_elector = [login_required(login_url='gest_usuario:login'),
                      group_required('elector'),
                      estado_confirmacion_no_required()]

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
            gen_cuentas_e(request.POST.getlist('elector_enabled'),
                          reverse('gest_usuario:cinfirmar'))
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


@method_decorator(decorators_elector, name='dispatch')
class ConfirmarCuenta(FormView):
    form_class = ClaveForm
    template_name = 'utils/create.html'
    # success_url = '#'

    def dispatch(self, request, *args, **kwargs):
        self.user = get_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            clave = form.cleaned_data.get('clave')
            self.user.set_password(clave)
            self.user.save()
            update_session_auth_hash(request, self.user)
            actualizar_cuentaelector(self.user.cuentaelector)
            # https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
            return redirect('bienvenida:bienvenida')
        else:
            context = self.get_context_data(**kwargs)
            # messages.error(request, 'Please correct the error below.')
            context['form'] = form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Ingresar'
        # context['cancel_url'] = 'gest_cifrado:ini-privada-i'
        # esta url necesita argumento pk
        context['cancel_url'] = 'bienvenida:bienvenida'
        context['card_title'] = 'Crea una clave para inicializar el descifrado'
        return context
