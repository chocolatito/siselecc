from django.shortcuts import redirect  # render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Urna
from .utils import (get_urna,
                    inciar_urna,
                    autorizar_elector,
                    retirar_elector,
                    es_autoridad,
                    get_padronelector)
from ..gest_preparacion.models import Mesa, PadronElector
from ..utils import group_required

# Create your views here.
decorators = [login_required(login_url='gest_usuario:login'), group_required('staff',)]


@method_decorator(decorators, name='dispatch')
class IniMesa(DetailView):
    model = Mesa
    template_name = 'gest_votacion/ini_mesa.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ver hora
        if es_autoridad(self.object, request.user):
            if self.object.estado_mesa == 2:
                # La mesa esta PREPARADA
                return super().dispatch(request, *args, **kwargs)
            elif self.object.estado_mesa == 3:
                # SI la mesa esta INICIADA
                return redirect(self.object.get_absolute_url_mesa_ini())
        else:
            # La mesa puede estar LISTA, OPERATIVA, CERRADA, CREADA, CON AUTORIDAD
            return redirect('bienvenida:bienvenida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Mesa'
        context['page_title_heading'] = 'Mesa de Votación'
        return context


@method_decorator(decorators, name='dispatch')
class MesaIni(DetailView):
    model = Mesa
    template_name = 'gest_votacion/mesa_ini.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ver hora
        if es_autoridad(self.object, request.user):
            if self.object.estado_mesa == 3:
                # LA MESA ESTA INICIADA
                return super().dispatch(request, *args, **kwargs)
            elif self.object.estado_mesa in [4, 5]:
                # LA MESA ESTA LISTA u OPERATIVA
                return redirect(self.object.get_absolute_url_mesa_ope())
            elif self.object.estado_mesa == 2:
                # LA MESA ESTA PREPARADA
                return redirect(self.object.get_absolute_url_ini())
            else:
                # LA MESA PUEDE ESTAR CERRADA, CREADA, CON AUTORIDAD
                return redirect('bienvenida:bienvenida')
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if self.object.urna.estado_urna:
            return redirect(self.object.get_absolute_url_mesa_ope())
        else:
            return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mesa de Votación'
        context['page_title_heading'] = 'Mesa de Votación'
        context['urna'] = get_urna(self.object)
        if context['urna'].estado_urna:
            context['padron'] = []
        return context


@method_decorator(decorators, name='dispatch')
class MesaOpe(DetailView):
    model = Mesa
    template_name = 'gest_votacion/mesa_ope.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ver hora
        if es_autoridad(self.object, request.user):
            if self.object.estado_mesa in [4, 5]:
                # LA MESA ESTA LISTA u OPERATIVA
                if self.object.estado_mesa == 5:
                    # LA MESA ESTA OPERATIVA
                    self.padronelector = get_padronelector(self.object)

                return super().dispatch(request, *args, **kwargs)
            elif self.object.estado_mesa == 3:
                # LA MESA ESTA INICIADA
                return redirect(self.object.get_absolute_url_mesa_ini())
            elif self.object.estado_mesa == 2:
                # LA MESA ESTA PREPARADA
                return redirect(self.object.get_absolute_url_ini())
            else:
                # LA MESA PUEDE ESTAR CERRADA, CREADA o CON AUTORIDAD
                return redirect('bienvenida:bienvenida')
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        """EL USUARIO SOLICITA AUTORIZAR AL ELECTOR"""
        return redirect(reverse('gest_votacion:autorizar', args=[request.POST['btn']]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mesa de Votación'
        context['page_title_heading'] = 'Mesa de Votación'
        if self.object.estado_mesa == 5:
            context['padronelector'] = self.padronelector
            context['thead_values'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Estado']
        else:
            context['inicio'] = self.object.eleccion.hora_inicio
        context['urna'] = self.object.urna
        return context


class AutorizarElector(DetailView):
    model = PadronElector
    template_name = 'gest_votacion/autorizar.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mesa = self.object.padron.eleccion.mesa
        self.estado_urna = self.mesa.urna.estado_urna
        # FALTA CONTROLAR QUE EL ELECTOR NO TENGA ESTADO 2
        if es_autoridad(self.object, request.user):
            if self.mesa.estado_mesa == 4:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('bienvenida:bienvenida')
        else:
            return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if self.estado_urna == 1:
            print('HAY QUE AUTORIZAR')
            autorizar_elector(self.object, self.mesa.urna)
        elif self.estado_urna == 6:
            retirar_elector(self.object, self.mesa.urna)
            return redirect(self.mesa.get_absolute_url_mesa_ope())
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesa'] = self.mesa
        context['estado_urna'] = self.mesa.urna.estado_urna
        return context


class IniUrna(TemplateView):
    template_name = 'gest_votacion/ini_urna.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        urna = inciar_urna(request.POST['codigo'])
        if urna:
            print('\nSE REDIRECCIONA A URNA LIBRE\n')
            return redirect(urna.get_absolute_url_urna_ope())
        else:
            return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_of_the_document'] = 'Iniciar Urna'
        context['page_title_heading'] = 'Iniciar Urna'
        return context


class UrnaOpe(DetailView):
    model = Urna
    template_name = 'gest_votacion/urna_ope.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ver hora
        if self.object.estado_urna == 0:
            return redirect(self.object.get_absolute_url_ini())
        else:
            if self.object.estado_urna in [1, 2, 5, 6]:
                # self.object.estado_urna == 1 or self.object.estado_urna == 2 or self.object.estado_urna == 5:
                return super().dispatch(request, *args, **kwargs)
            elif self.object.estado_urna == 3:
                self.boletas = self.object.mesa.eleccion.boleta_set.all()
                return super().dispatch(request, *args, **kwargs)
            elif self.object.estado_urna == 4:
                self.boleta = self.object.mesa.eleccion.boleta_set.get(id=kwargs['id_boleta'])
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        if self.object.estado_urna == 2:
            self.object.estado_urna = 3
            self.object.save()
        elif self.object.estado_urna == 3:
            self.object.estado_urna = 4
            self.object.save()
            return redirect('gest_votacion:urna-confirmar',
                            pk=self.object.id,
                            id_boleta=request.POST['btn-boleta'])
        elif self.object.estado_urna == 4:
            if 'btn-confirmar' in request.POST:
                self.object.estado_urna = 5
                self.object.save()
            elif 'btn-cancelar' in request.POST:
                self.object.estado_urna = 3
                self.object.save()
            return redirect(self.object.get_absolute_url_urna_ope())
        elif self.object.estado_urna == 5:
            self.object.estado_urna = 6
            self.object.save()
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Urna LIBRE'
        context['page_title_heading'] = 'Urna LIBRE'
        if self.object.estado_urna == 3:
            context['boletas'] = self.boletas
        elif self.object.estado_urna == 4:
            context['boleta'] = self.boleta
        context['estados_pasivos'] = [1, 2, 6]
        return context
