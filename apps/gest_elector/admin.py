from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Elector
# Register your models here.

# _Elector


class ElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'dni', 'nombres', 'apellidos', 'correo', 'cuenta_u')


admin.site.register(Elector, ElectorAdmin)
