from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Eleccion, Padron, Mesa, PadronElector, Candidato
# Register your models here.


class EleccionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('titulo', 'id', 'fecha', 'hora_inicio', 'hora_fin', 'etapa', 'slug')


class PadronAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'eleccion',)


class MesaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'estado_mesa', 'cuenta', 'eleccion',)


class CandidatoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Eleccion, EleccionAdmin)
admin.site.register(Padron, PadronAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(PadronElector)
admin.site.register(Candidato, CandidatoAdmin)
