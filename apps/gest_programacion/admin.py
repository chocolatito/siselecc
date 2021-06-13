from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Boleta
# Register your models here.


class BoletaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'n', 'indice', 'vector_candidato', 'eleccion', 'candidato')


admin.site.register(Boleta, BoletaAdmin)
