from datetime import datetime, time
from django.forms import NumberInput, TimeField
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from ..gest_preparacion.models import Eleccion

# Cargo


class EleccionForm(ModelForm):
    hora_inicio = TimeField(widget=NumberInput(attrs={'type': 'time'}))
    hora_fin = TimeField(widget=NumberInput(attrs={'type': 'time'}))

    class Meta:
        model = Eleccion
        fields = ['hora_inicio', 'hora_fin', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

# https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-a-specific-field-attribute

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if (time(8, 0, 0) <= hora_inicio):
            return hora_inicio
        else:
            raise ValidationError('Hora de inicio debe ser mayor a la 8 horas')

    def clean_hora_fin(self):
        hora_fin = self.cleaned_data.get('hora_fin')
        if hora_fin <= time(20, 0, 0):
            return hora_fin
        else:
            raise ValidationError('Hora de fin debe ser menor a la 20 horas')

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if hora_fin and hora_inicio:
            if hora_fin < hora_inicio:
                raise ValidationError({'hora_fin': ValidationError(
                    'Hora de fin debe ser mayor a la hora de inicio')})
