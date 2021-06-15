from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Clave, SecuenciaPrimo
# Register your models here.


class SecuenciaPrimoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['indice']


admin.site.register(SecuenciaPrimo, SecuenciaPrimoAdmin)

admin.site.register(Clave)
