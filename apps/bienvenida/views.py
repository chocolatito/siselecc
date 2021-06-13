# from django.shortcuts import render
from django.views.generic import TemplateView
# from ..gest_cifrado.utils import generar_secuencias  # eliminar

# Create your views here.

#decorators = [login_required(login_url='gest_usuario:login'), ]


# @method_decorator(decorators, name='dispatch')
class Bienvenida(TemplateView):
    template_name = "bienvenida/bienvenida.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bienvenido'
        context['iterador'] = [x for x in range(20)]
        return context
