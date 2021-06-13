from django.contrib import admin
from .models import Urna

# Register your models here.
# Register your models here.
#


class UrnaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_inicio', 'estado_urna', 'creacion', 'mesa')


admin.site.register(Urna, UrnaAdmin)
