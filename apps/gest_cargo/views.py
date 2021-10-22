# from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # , reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required

from .forms import CargoForm
from .models import Cargo
from ..utils import set_active, set_active_field, get_queryset_by_state, group_required
# Create your views here.


# ____________________________________________
# _Cargo
#  decorators = [login_required(login_url='gest_usuario:login'), ]
decorators = [login_required(login_url='gest_usuario:login'),
group_required('staff',),]


@ method_decorator(decorators, name='dispatch')
class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'utils/create.html'
    success_url = reverse_lazy('gest_cargo:listado')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                return HttpResponseRedirect(self.object.get_absolute_url())
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Registrar'
        context['cancel_url'] = 'gest_cargo:listado'
        context['card_title'] = 'Agregar un Cargo'
        context['object_list'] = Cargo.objects.all()
        if context['object_list']:
            context['card2_title'] = 'Cargo ya registrados'
        else:
            context['card2_title'] = 'Primer Registro'
            context['card_message'] = "No hay cargos registrados en el sistema"
        return context


@ method_decorator(decorators, name='dispatch')
class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'utils/create.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Editar datos del cargo"
        context['cancel_url'] = 'gest_cargo:listado'
        context['submit_button'] = 'Actualizar'
        return context


@ method_decorator(decorators, name='dispatch')
class CargoListView(ListView):
    model = Cargo
    template_name = 'gest_cargo/cargo_list.html'

    def dispatch(self, request, *args, **kwargs):
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
        context['title'] = "Listado de Cargo"
        context['message_no_queryset'] = 'No hay cargos registrados'
        context['thead_values'] = ['Cargo', 'Descripción', 'Estado de cargo', ]
        context['url_listado'] = 'gest_cargo:listado'
        context['url_agregar'] = 'gest_cargo:agregar'
        context['url_detalle'] = 'gest_cargo:detalle'
        context['url_actualizar'] = 'gest_cargo:actualizar'
        context['snippet_accion_table'] = 'gest_cargo/snippets/snippet_accion_table.html'
        if 'estado' in self.request.GET:
            context['estado'] = self.request.GET['estado']
        context['text_badge_dark'] = f'Listado de cargos registrados'
        return context


@method_decorator(decorators, name='dispatch')
class CargoDetailView(DetailView):
    model = Cargo
    template_name = 'gest_cargo/cargo_detail.html'

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
        context['url_listado'] = 'gest_cargo:listado'
        # context['list_url'] = reverse_lazy('eleccion:cargo-list')
        context['title'] = "Detalle del Cargo"
        context['page_title_heading'] = self.object.__str__()
        context['url_actualizar'] = 'gest_cargo:actualizar'
        context['snippet_accion_detail'] = 'gest_cargo/snippets/snippet_accion_detail.html'
        context['text_badge_dark'] = f'Detalles del cargo {self.object}'
        # context['title'] = self.object.__str__()
        #context['eleccion_set'] = self.object.eleccion_set.all()
        #context['active_url'] = 'eleccion:active_cargo'
        return context
