from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Urna, Voto

# Register your models here.
# Register your models here.
#


class UrnaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'codigo_inicio', 'estado_urna', 'creacion', 'mesa')


class VotoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'urna')


admin.site.register(Urna, UrnaAdmin)
admin.site.register(Voto, VotoAdmin)
