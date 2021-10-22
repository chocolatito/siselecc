from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .utils import get_escrutinio, get_total_votos, actualiar_fallidas
from ..gest_preparacion.models import Eleccion, Padron
# Create your views here.


class Bienvenida(TemplateView):
    template_name = "bienvenida/bienvenida.html"

    def dispatch(self, request, *args, **kwargs):
        # actualiar fallidas
        actualiar_fallidas(Eleccion.objects.filter(etapa=1))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bienvenido'
        # Elecciones programadas, en curso y cerradas
        context['proximas'] = Eleccion.objects.filter(etapa__in=[1, 2])
        context['en_curso'] = Eleccion.objects.filter(etapa=3)
        context['cerradas'] = Eleccion.objects.filter(etapa__in=[4, 5, 6])
        context['thead_values'] = ['Titulo', 'Fecha', 'Acciones', ]
        context['thead_values_encurso'] = ['Titulo', 'Fecha', 'Inicio-Cierre', ]
        context['text_badge_dark'] = 'Página de Inicio - Resumen de la actividad electoral del sistema'
        return context


class Resultado(DetailView):
    model = Eleccion
    template_name = 'bienvenida/resultado.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.etapa == 6:
            self.boletas = self.object.boleta_set.exclude(indice=0)
            self.v_resultado = self.object.resultado.vector_resultado
            self.is_staff = bool(request.user.groups.filter(name='staff'))
            # Generar el resultado
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenida:bienvenida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gestionar contex
        context['title'] = 'Resultados'
        context['page_title_heading'] = f'{self.object} - Resultados'
        context['escrutinio'] = get_escrutinio(self.boletas,
                                               self.v_resultado,
                                               get_total_votos(self.v_resultado))
        context['snippet_accion_detail'] = 'bienvenida/snippets/snippet_accion_detail.html'
        context['is_staff'] = self.is_staff
        context['text_badge_dark'] = f"{self.object}"
        return context


class DetallesCerrada(DetailView):
    model = Eleccion
    template_name = 'bienvenida/detalle_cerrada.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.etapa in [4, 5]:
            # Generar el resultado
            self.is_staff = bool(request.user.groups.filter(name='staff'))
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenida:bienvenida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gestionar contex
        # title
        # page_title_heading
        context['padron'] = self.object.padron
        context['urna'] = self.object.mesa.urna
        context['snippet_accion_detail'] = 'bienvenida/snippets/snippet_accion_detail.html'
        context['is_staff'] = self.is_staff
        context['text_badge_dark'] = f"{self.object}"
        # DEBERIA INCLUIR LA HORA EXACTA DE CIERRE DE VOTACIÓN
        context['detali_info'] = self.object.get_detali_info_proxima()
        return context


class DetallesProxima(DetailView):
    model = Eleccion
    template_name = 'bienvenida/detalle_proxima.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.etapa in [1, 2]:
            #
            self.is_staff = bool(request.user.groups.filter(name='staff'))
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('bienvenida:bienvenida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gestionar contex
        # title
        # page_title_heading
        context['snippet_accion_detail'] = 'bienvenida/snippets/snippet_accion_detail.html'
        context['is_staff']=self.is_staff
        context['detali_info'] = self.object.get_detali_info_proxima()
        context['text_badge_dark'] = f"{self.object}"
        return context


class ConsultaPadron(DetailView):
    model = Eleccion
    template_name = 'bienvenida/padron_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.object.padron.padronelector_set.all()
        self.is_staff = bool(request.user.groups.filter(name='staff'))
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet_accion_detail'] = 'bienvenida/snippets/snippet_accion_padron.html'
        context['thead_values'] = ['DNI', 'Apellido/s', 'Nombre/s', 'Estado']
        context['is_staff']=self.is_staff
        context['text_badge_dark'] = f"{self.object}"
        context['object_list'] = self.object_list
        context['snippet_accion_table'] = 'utils/blank.html'
        return context
