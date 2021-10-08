from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy  # , reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import EleccionForm
from .models import Eleccion, Padron, Mesa, Candidato
from .utils import (gen_padron_mesa,
                    get_disponibles,
                    get_elector_exclude_padron,
                    admi_elector2padron,
                    staff_list,
                    agregar_candidato, set_estado_postulacion)
from ..utils import (get_queryset_by_state,
                     group_required,
                     set_active,
                     set_active_field)


# Create your views here.
# ____________________________________________
# _Eleccion
# _Padron
# _Mesa
# _Candidato
# ____________________________________________

decorators = [login_required(login_url='gest_usuario:login'), group_required('staff',)]
# decorators = [login_required(login_url='gest_usuario:login'), ]


# ____________________________________________
# _Eleccion
@ method_decorator(decorators, name='dispatch')
class EleccionCreateView(CreateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = 'utils/create_select.html'
    success_url = reverse_lazy('bienvenida:bienvenida')

    def post(self, request, *args, **kwargs):
        form = EleccionForm(request.POST)
        if form.is_valid():
            # return redirect(self.success_url)
            return HttpResponseRedirect(gen_padron_mesa(form.save()).get_absolute_url())
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button'] = 'Registrar'
        context['cancel_url'] = 'gest_preparacion:listado'
        context['card_title'] = 'Agregar una Eleccion'
        return context


@ method_decorator(decorators, name='dispatch')
class EleccionUpdateView(UpdateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = 'utils/create.html'
    # success_url = reverse_lazy('gest_cargo:listado')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.etapa == 0:
            return super().dispatch(request, *args, **kwargs)
        else:
            print('NOSE PUEDE ACTUALIZAR')
            return redirect('bienvenida:bienvenida')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del cargo"
        context['cancel_url'] = 'gest_preparacion:listado'
        context['submit_button'] = 'Actualizar'
        return context


@ method_decorator(decorators, name='dispatch')
class EleccionListView(ListView):
    model = Eleccion
    template_name = 'gest_preparacion/eleccion_list.html'

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
        context['title'] = 'Listado de Eleccion'
        context['page_title_heading'] = 'Eleccion'
        context['message_no_queryset'] = 'No hay elecciones registradas'
        context['thead_values'] = ['Titulo',
                                   'Fecha de realización',
                                   'Horarios de Inicio-Fin',
                                   'Etapa', ]
        context['url_listado'] = 'gest_preparacion:listado'
        context['url_agregar'] = 'gest_preparacion:agregar'
        context['url_detalle'] = 'gest_preparacion:detalle'
        context['url_actualizar'] = 'gest_preparacion:actualizar'
        context['snippet_accion_table'] = 'gest_preparacion/snippets/snippet_accion_table.html'

        return context


@method_decorator(decorators, name='dispatch')
class EleccionDetailView(DetailView):
    model = Eleccion
    template_name = 'gest_preparacion/eleccion_detail.html'

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
        context['url_listado'] = 'gest_preparacion:listado'
        context['title'] = 'Detalle del Eleccion'
        context['page_title_heading'] = self.object.__str__()
        context['url_actualizar'] = 'gest_preparacion:actualizar'
        context['padron'] = Padron.objects.get(eleccion=self.object)
        context['mesa'] = Mesa.objects.get(eleccion=self.object)
        # DEBERIA SER ncandidatos
        context['candidato'] = self.object.candidatos().count()
        context['snippet_accion_detail'] = 'gest_preparacion/snippets/snippet_accion_detail.html'
        return context


# ____________________________________________
# _Padron
@method_decorator(decorators, name='dispatch')
class PadronDetailView(DetailView):
    model = Padron
    template_name = 'gest_preparacion/padron_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(f"\n\n{request.POST.getlist('no_incluidos')}\n\n")
        print(f"\n\n{request.POST.getlist('incluidos')}\n\n")
        if request.POST['button'] == 'agregar':
            admi_elector2padron(self.object,
                                request.POST.getlist('no_incluidos'),
                                'agregar')
        elif request.POST['button'] == 'quitar':
            admi_elector2padron(self.object,
                                request.POST.getlist('incluidos'),
                                'quitar')
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['url_listado'] = 'gest_preparacion:listado'
        context['title'] = 'Administración del Padron'
        context['page_title_heading'] = f'Corresponde a la {self.object.eleccion.__str__()}'
        context['no_incluidos'] = get_elector_exclude_padron(self.object.electores.all())
        context['thead_values'] = ['DNI', 'Nombre/s', 'Apellido/s']
        context['snippet_accion_detail'] = 'utils/blank.html'
        return context


# ____________________________________________
# _Mesa
@method_decorator(decorators, name='dispatch')
class MesaDetailView(DetailView):
    model = Mesa
    template_name = 'gest_preparacion/mesa_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            self.object.cuenta = User.objects.get(id=request.POST['staff-btn'])
            self.object.estado_mesa = 1
            self.object.save()
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title_heading'] = f'Corresponde a la {self.object.eleccion.__str__()}'
        context['snippet_accion_detail'] = 'utils/blank.html'
        context['staff_list'] = staff_list(self.object.cuenta)
        return context


# ____________________________________________
# _Candidato
@method_decorator(decorators, name='dispatch')
class AdministrarCandidatos(DetailView):
    model = Eleccion
    template_name = 'gest_preparacion/candidato_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'disponible' in request.POST:
            agregar_candidato(self.object, request.POST["disponible"])
        elif 'candidato' in request.POST:
            set_estado_postulacion(Candidato.objects.get(id=request.POST['candidato']))
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['url_listado'] = 'gest_preparacion:listado'
        context['title'] = 'Administración del Candidatos'
        context['page_title_heading'] = f'Elección::: {self.object.__str__()}'
        context['candidatos'] = self.object.candidato_set.all()
        context['disponibles'] = get_disponibles(context['candidatos'], 'elector')
        context['thead_values'] = ['DNI', 'Nombre/s', 'Apellido/s']
        context['snippet_accion_detail'] = 'utils/blank.html'
        return context
