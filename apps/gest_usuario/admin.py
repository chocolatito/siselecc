from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CuentaElector
# Register your models here.
#


class CuentaElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('creacion', 'confirmacion', 'estado_confirmacion', 'cuenta', 'elector')


admin.site.register(CuentaElector, CuentaElectorAdmin)
