from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from .models import CuentaElector
# Register your models here.
#

class CustonUserAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ('username', 'email', 'is_staff')


admin.site.unregister(User)
admin.site.register(User, CustonUserAdmin)


class CuentaElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('creacion', 'confirmacion', 'estado_confirmacion', 'cuenta', 'elector')


admin.site.register(CuentaElector, CuentaElectorAdmin)
