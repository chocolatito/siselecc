# from django.shortcuts import render
from django.views.generic import TemplateView
from ..gest_preparacion.models import Eleccion
# from ..gest_cifrado.utils import generar_secuencias  # eliminar

# Create your views here.

#decorators = [login_required(login_url='gest_usuario:login'), ]


# @method_decorator(decorators, name='dispatch')
class Bienvenida(TemplateView):
    template_name = "bienvenida/bienvenida.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bienvenido'
        # Elecciones programadas, en curso y cerradas
        context['proximas'] = Eleccion.objects.filter(etapa__in=[1, 2])
        context['en_curso'] = Eleccion.objects.filter(etapa=3)
        context['cerradas'] = Eleccion.objects.filter(etapa__in=[4, 5, 6])
        return context
