from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Elector

# Cargo


class ElectorForm(ModelForm):

    class Meta:
        model = Elector
        fields = ['dni', 'nombres', 'apellidos', 'correo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'


"""
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Elector.objects.filter(dni=dni):
            raise ValidationError('YA EXISTE UN ELECTOR REGISTRADO CON ESE DNI')
        else:
            return dni

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Elector.objects.filter(correo=correo):
            raise ValidationError('YA EXISTE UN ELECTOR REGISTRADO CON ESE CORREO')
        else:
            return correo

    def save(self, commit=True):
        object = super().save(commit=False)
        print(f'\nEl nuevo objeto:\t{object.dni}')
        if commit:
            object.save()
        return object
"""
