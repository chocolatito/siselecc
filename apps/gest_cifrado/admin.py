from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Clave, Resultado, Parcial  # , SecuenciaPrimo
# Register your models here.

"""
class SecuenciaPrimoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['indice']
    list_per_page = 10
admin.site.register(SecuenciaPrimo, SecuenciaPrimoAdmin)
"""


class ClaveAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['eleccion', 'cuenta']


class ResultadoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['eleccion', 'final', ]


class ParcialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['resultado', 'descifrado', 'fecha_hora', 'clave']


admin.site.register(Clave, ClaveAdmin)
admin.site.register(Resultado, ResultadoAdmin)
admin.site.register(Parcial, ParcialAdmin)
