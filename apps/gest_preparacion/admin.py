from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Eleccion, Padron, Mesa, PadronElector, Candidato
# Register your models here.


class EleccionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('titulo', 'id', 'fecha', 'hora_inicio', 'hora_fin', 'etapa', 'slug')


admin.site.register(Eleccion, EleccionAdmin)
admin.site.register(Padron)
admin.site.register(Mesa)
admin.site.register(PadronElector)
admin.site.register(Candidato)
