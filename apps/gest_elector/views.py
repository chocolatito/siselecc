from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy  # , reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import ElectorForm
from .models import Elector
from ..utils import set_active, get_queryset_by_state, set_active_field
# Create your views here.


# ____________________________________________
# _Elector
# decorators = [login_required, group_required('staff',)]
decorators = [login_required(login_url='gest_usuario:login'), ]


@ method_decorator(decorators, name='dispatch')
class ElectorCreateView(CreateView):
    model = Elector
    form_class = ElectorForm
    template_name = 'utils/create.html'
    success_url = reverse_lazy('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        form = ElectorForm(request.POST)
        if form.is_valid():
            # form.save(): return model.object
            return HttpResponseRedirect(form.save().get_absolute_url())
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Registrar'
        context['cancel_url'] = 'gest_elector:listado'
        context['card_title'] = 'Agregar un Elector'
        return context


@ method_decorator(decorators, name='dispatch')
class ElectorUpdateView(UpdateView):
    model = Elector
    form_class = ElectorForm
    template_name = 'utils/create.html'
    #success_url = reverse_lazy('gest_cargo:listado')

    def get_success_url(self):
        # return reverse('gest_cargo:detalle', kwargs={'pk': self.object.id})
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del cargo"
        context['cancel_url'] = 'gest_elector:listado'
        context['submit_button'] = 'Actualizar'
        return context


@ method_decorator(decorators, name='dispatch')
class ElectorListView(ListView):
    model = Elector
    template_name = 'gest_elector/elector_list.html'

    def dispatch(self, request, *args, **kwargs):
        # print(request.GET)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """"""
        if 'estado' in self.request.GET:
            return get_queryset_by_state(self.model, self.request.GET['estado'])
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            set_active(self.model,
                       request.POST['object_id'],
                       'True' == request.POST['active'])
        except KeyError:
            print('Where is my flag?')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Elector'
        context['page_title_heading'] = 'Elector'
        context['message_no_queryset'] = 'No hay electores registrados'
        context['thead_values'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Posee cuenta?', ]
        context['url_listado'] = 'gest_elector:listado'
        context['url_agregar'] = 'gest_elector:agregar'
        context['url_detalle'] = 'gest_elector:detalle'
        context['url_actualizar'] = 'gest_elector:actualizar'
        return context


@method_decorator(decorators, name='dispatch')
class ElectorDetailView(DetailView):
    model = Elector
    template_name = 'gest_elector/elector_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            set_active_field(self.object, 'True' == request.POST['active'])
        except KeyError:
            print('Where is my flag?')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_listado'] = 'gest_elector:listado'
        context['title'] = 'Detalle del Elector'
        context['page_title_heading'] = self.object.__str__()
        context['url_actualizar'] = 'gest_elector:actualizar'
        # context['title'] = self.object.__str__()
        #context['eleccion_set'] = self.object.eleccion_set.all()
        #context['active_url'] = 'eleccion:active_elector'
        return context
