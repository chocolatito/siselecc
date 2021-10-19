from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .utils import get_escrutinio, get_total_votos
from ..gest_preparacion.models import Eleccion
# Create your views here.


class Bienvenida(TemplateView):
    template_name = "bienvenida/bienvenida.html"

    def dispatch(self, request, *args, **kwargs):
        #
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
        return context


class DetallesCerrada(DetailView):
    model = Eleccion
    template_name = 'bienvenida/detalle_cerrada.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.etapa in [4, 5]:
            # Generar el resultado
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
        return context
