from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import ClaveForm
from .utils import (verificar_user_elector,
                    generar_Cpublica,
                    verificar_user_clave,
                    crear_resultado, generar_parciales)
from ..utils import group_required, get_user
from ..gest_preparacion.models import Eleccion
from ..gest_preparacion.utils import get_eleccion
from ..gest_votacion.utils import es_autoridad

# Create your views here.

decorators = [login_required(login_url='gest_usuario:login'),
              group_required('staff', 'elector')]


@method_decorator(decorators, name='dispatch')
class GestorCifradoView(TemplateView):
    template_name = 'gest_cifrado/bienvenido.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_of_the_document'] = 'Gestor de Cifrado'
        context['page_title_heading'] = 'Gestor de Cifrado'
        context['programadas'] = Eleccion.objects.filter(etapa=1)
        context['cerradas'] = Eleccion.objects.filter(etapa=5)
        return context


# _Publica
@ method_decorator(decorators, name='dispatch')
class IniPublica_I(DetailView):
    model = Eleccion
    template_name = 'gest_cifrado/ini_publica_i.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Se debe verificar que la eleccion este programada
        if self.object.etapa == 1:
            return super().dispatch(request, *args, **kwargs)
        elif self.object.etapa == 2:
            return redirect(self.object.get_absolute_url())
        else:
            return redirect('bienvenido:bienvenido')

    def post(self, request, *args, **kwargs):
        if request.POST['btn'] == 'candidato':
            if verificar_user_elector(get_user(request.user.username),
                                      self.object.candidato_set.filter(estado_postulacion=True)):
                print(f'Candidatos\n___> {request.user.username}\n')
                print('SE DEBE REDIRECCIONAR A UN FORMULARIO PARA INGRESAR LA CLAVE')
                return redirect('gest_cifrado:ini-publica-ii', pk=self.object.id)
            else:
                print(f'No es Candidatos\n___> {request.user.username}\n')
        elif request.POST['btn'] == 'autoridad':
            # if self.object.mesa.cuenta.username == request.user.username:
            if es_autoridad(self.object.mesa, request.user):
                print(f'Autoridad\n___> {request.user.username}\n')
                print('SE DEBE REDIRECCIONAR A UN FORMULARIO PARA INGRESAR LA CLAVE')
                return redirect('gest_cifrado:ini-publica-ii', pk=self.object.id)
            else:
                print(f'No es Autoridad\n___> {request.user.username}\n')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Eleccion xyz'
        context['page_title_heading'] = 'Listado de Eleccion xyz'
        context['message_no_queryset'] = 'No hay elecciones registradas'
        context['url_listado'] = 'gest_preparacion:listado'
        context['url_agregar'] = 'gest_preparacion:agregar'
        context['url_detalle'] = 'gest_preparacion:detalle'
        context['url_actualizar'] = 'gest_preparacion:actualizar'
        context['snippet_accion_table'] = 'gest_preparacion/snippets/snippet_accion_table.html'
        return context


@ method_decorator(decorators, name='dispatch')
class IniPublica_II(FormView):
    # specify the Form you want to use
    form_class = ClaveForm

    # sepcify name of template
    template_name = 'utils/create.html'
    success_url = reverse_lazy('gest_cifrado:gest_cifrado')

    def dispatch(self, request, *args, **kwargs):
        #self.object = get_eleccion(kwargs['pk'])
        if verificar_user_clave(get_eleccion(kwargs['pk']),
                                get_user(request.user.username)):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if generar_Cpublica(form.cleaned_data.get('clave'),
                                tuple(int(x) for x in form.cleaned_data.get('color')),
                                get_user(request.user.username),
                                get_eleccion(kwargs['pk'])):
                # return redirect(self.object.get_absolute_url())
                return redirect('bienvenida:bienvenida')
            else:
                return redirect(self.success_url)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Ingresar'
        context['card_title'] = 'Crea una clave para inicializar el cifrado'
        return context


# _Conteo
@ method_decorator(decorators, name='dispatch')
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
            return redirect('bienvenido:bienvenido')

    def post(self, request, *args, **kwargs):
        if 'btn-iniciar' in request.POST:
            #
            resultado = crear_resultado(self.object)
            # se deben obtener las sumas parciales
            if generar_parciales(resultado, self.object.clave_set.all()):
                self.object.etapa = 5
                self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# _Privada
@ method_decorator(decorators, name='dispatch')
class IniPrivada_I(DetailView):
    model = Eleccion
    template_name = 'gest_cifrado/ini_privada_i.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Se debe verificar que la eleccion este cerrada
        if self.object.etapa == 5:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenido:bienvenido')

    def post(self, request, *args, **kwargs):
        if request.POST['btn'] == 'candidato':
            if verificar_user_elector(get_user(request.user.username),
                                      self.object.candidato_set.filter(estado_postulacion=True)):
                return redirect('gest_cifrado:ini-publica-ii', pk=self.object.id)
            else:
                print(f'No es Candidatos\n___> {request.user.username}\n')
        elif request.POST['btn'] == 'autoridad':
            if self.object.mesa.cuenta.username == request.user.username:
                print(f'Autoridad\n___> {request.user.username}\n')
                print('SE DEBE REDIRECCIONAR A UN FORMULARIO PARA INGRESAR LA CLAVE')
                return redirect('gest_cifrado:ini-publica-ii', pk=self.object.id)
            else:
                print(f'No es Autoridad\n___> {request.user.username}\n')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
