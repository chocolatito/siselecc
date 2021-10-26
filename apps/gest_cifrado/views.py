from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import ClaveForm
from .utils import (es_candidato,
                    generar_Cpublica,
                    get_clave_and_color,
                    verificar_user_clave,
                    crear_resultado, generar_parciales,
                    privada_iniciada,
                    actualizar_resultado)
from ..utils import group_required, get_user, estado_confirmacion_required
from ..gest_preparacion.models import Eleccion
from ..gest_preparacion.utils import get_eleccion
from ..gest_votacion.utils import es_autoridad

# Create your views here.
# _Publica
# _Conteo
# _Privada

decorators = [login_required(login_url='gest_usuario:login'),
              group_required('staff')]
decorators_elector = [login_required(login_url='gest_usuario:login'),
                      group_required('staff', 'elector'),
                      estado_confirmacion_required()]


@method_decorator(decorators_elector, name='dispatch')
class GestorCifradoView(TemplateView):
    template_name = 'gest_cifrado/bienvenido.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programadas'] = Eleccion.objects.filter(etapa=1)
        context['cerradas'] = Eleccion.objects.filter(etapa=5)
        context['text_badge_dark'] = 'Gestor de claves de Cifrado'

        return context


# _Publica
@method_decorator(decorators_elector, name='dispatch')
class IniPublica_I(DetailView):
    model = Eleccion
    template_name = 'gest_cifrado/ini_publica_i.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Se debe verificar que la eleccion este programada
        if self.object.etapa == 1:
            if self.object.claves_atiempo():
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'SE DEBE ACTUALIZAR LA PROGRAMACIÓN DE HORARIOS. El Staff debe reprogramar el horarió de inicio de votación a una hora mayor a la hora actual')
                return redirect('gest_cifrado:gest_cifrado')
        elif self.object.etapa == 2:
            return redirect(self.object.get_absolute_url())
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if request.POST['btn'] == 'candidato':
            if es_candidato(get_user(request.user), self.object.candidatos()):
                # return redirect('gest_cifrado:ini-publica-ii', pk=self.object.id)
                return redirect(self.object.get_cifrado_ii_url())
            else:
                print(f'No es Candidatos\n___> {request.user.username}\n')
        elif request.POST['btn'] == 'autoridad':
            # if self.object.mesa.cuenta.username == request.user.username:
            if es_autoridad(self.object.mesa, request.user):
                print(f'Autoridad\n___> {request.user.username}\n')
                return redirect(self.object.get_cifrado_ii_url())
            else:
                print(f'No es Autoridad\n___> {request.user.username}\n')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Eleccion xyz'
        context['snippet_accion_table'] = 'gest_preparacion/snippets/snippet_accion_table.html'
        return context


@method_decorator(decorators_elector, name='dispatch')
class IniPublica_II(FormView):
    form_class = ClaveForm
    template_name = 'utils/create.html'
    success_url = reverse_lazy('gest_cifrado:gest_cifrado')

    def dispatch(self, request, *args, **kwargs):
        self.object = get_eleccion(kwargs['pk'])
        self.user = get_user(request.user)
        if verificar_user_clave(self.object, get_user(request.user)):
            # El usuario no posee clave inicializada
            return super().dispatch(request, *args, **kwargs)
        else:
            # El usuario ya ha inicializado su clave
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if generar_Cpublica(form.cleaned_data.get('clave'),
                                tuple(int(x) for x in form.cleaned_data.get('color')),
                                self.user, self.object):
                messages.success(request, 'EXCELENTE La inicialización de la clave ha sido un exito')
                messages.success(request, 'Ahora podra inicializar la mesa de votación y su correspondiente urna')
                return redirect(self.object.get_absolute_url())
            else:
                messages.success(request, 'EXCELENTE La inicialización de la clave ha sido un exito!!!')
                return redirect(self.object.get_proxima_url())
        else:
            context = self.get_context_data(**kwargs)
            context['form']=form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Ingresar'
        context['cancel_url'] = 'gest_cifrado:gest_cifrado'
        context['card_title'] = 'Crea una clave para inicializar el cifrado'
        return context


# _Conteo
@method_decorator(decorators, name='dispatch')
class IniConteo(DetailView):
    model = Eleccion
    template_name = 'gest_cifrado/ini_conteo.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if es_autoridad(self.object.mesa, request.user):
            # Se debe verificar que la eleccion este cerrada
            if self.object.etapa == 4:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(self.object.get_absolute_url())
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if 'btn-iniciar' in request.POST:
            #
            resultado = crear_resultado(self.object)
            if self.object.mesa.urna.voto_set.all():
                # La eleccion posee al menos 1 voto
                claves = self.object.get_claves_candidatos()
                # se deben obtener las sumas parciales
                if generar_parciales(resultado, claves):
                    self.object.etapa = 5
                    self.object.save()
            else:
                resultado.final = True
                resultado.vector_resultado = ['0', '0', '0']
                resultado.save()
                self.object.etapa = 6
                self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# _Privada
@method_decorator(decorators_elector, name='dispatch')
class IniPrivada_I(DetailView):
    model = Eleccion
    template_name = 'gest_cifrado/ini_privada_i.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Se debe verificar que la eleccion este cerrada
        if self.object.etapa == 5:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if request.POST['btn'] == 'candidato':
            if es_candidato(get_user(request.user), self.object.candidatos()):
                # El usuarios es un candidato de la elección
                if privada_iniciada(self.object, get_user(request.user)):
                    # El usuario ya ha inicializado la clave privad
                    messages.error(request, 'ERROR La clave  ya ha sido inicializada')
                    return redirect(self.object.get_absolute_url())
                else:
                    # El usuario puede inicializar la clave privada
                    return redirect('gest_cifrado:ini-privada-ii', pk=self.object.id)
            else:
                messages.error(request, 'ERROR Este usuario no esta registrado como candidato para esta elección')
        elif request.POST['btn'] == 'autoridad':
            if self.object.mesa.cuenta.username == request.user.username:
                # Es autoridad
                if self.object.resultado.parciales == self.object.n_candidatos():
                    # todos los candidatos ya han iniciado sus claves de descifrado
                    # SE DEBE REDIRECCIONAR A UN FORMULARIO PARA INGRESAR LA CLAVE
                    return redirect('gest_cifrado:ini-privada-ii', pk=self.object.id)
                else:
                    return redirect('bienvenida:bienvenida')
            else:
                messages.error(request,
                               'ERROR Este usuario no esta registrado como autoridad de mesa para esta elección')
                return redirect(request.META['HTTP_REFERER'])
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(decorators_elector, name='dispatch')
class IniPrivada_II(FormView):
    form_class = ClaveForm
    template_name = 'utils/create.html'
    success_url = reverse_lazy('gest_cifrado:gest_cifrado')

    def dispatch(self, request, *args, **kwargs):
        self.eleccion = get_eleccion(kwargs['pk'])
        if verificar_user_clave(self.eleccion, get_user(request.user)):
            # El usuario no posee clave inicializada
            messages.error(request, 'ERROR Esta cuenta no verifica clave para esta elección')
            return redirect('bienvenida:bienvenida')
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # clave = form.cleaned_data.get('clave')
            # color = tuple(int(x) for x in form.cleaned_data.get('color'))
            clave, color = get_clave_and_color(form.cleaned_data)
            if actualizar_resultado(clave, color, get_user(request.user), self.eleccion):
                messages.success(request, 'EXCELENTE La inicialización de la clave ha sido un exito!!!')
                return redirect(self.eleccion.get_cerrada_url())
            else:
                messages.error(request, 'ERROR Clave y/o Color ingresado/s incorrecto/s')
                return redirect(self.eleccion.get_descifrado_url())
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Ingresar'
        context['cancel_url'] = 'gest_cifrado:gest_cifrado'
        context['card_title'] = 'Crea una clave para inicializar el descifrado'
        return context
