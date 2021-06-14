from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .forms import EleccionForm
from .utils import actualizar_etapa
from ..utils import group_required
from ..gest_preparacion.models import Eleccion

# Create your views here.

decorators = [login_required(login_url='gest_usuario:login'), group_required('staff',)]


@ method_decorator(decorators, name='dispatch')
class AdmProgramacion(UpdateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = 'utils/create.html'
    # success_url = reverse_lazy('gest_cargo:listado')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.es_programable():
            # FALTAN MENOS DE UN DIA PARA REALIZAR LA ELECCION
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.object.get_absolute_url())

    def post(self, request, *args, **kwargs):
        form = EleccionForm(request.POST, instance=self.object)
        if form.is_valid():
            return HttpResponseRedirect(actualizar_etapa(form.save()).get_absolute_url())
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Administrar programación"
        context['submit_button'] = 'Programar'
        return context
