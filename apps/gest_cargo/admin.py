from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Cargo
# Register your models here.
#


class CargoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


admin.site.register(Cargo, CargoAdmin)
