# from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class Bienvenida(TemplateView):
    template_name = "system_info/bienvenida.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Info del Sistema'
        context['text_badge_dark'] = 'Información sobre el sistema'
        return context
