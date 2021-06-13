from django.forms import DateField, NumberInput
from django.forms import ModelForm
from .models import Eleccion
from ..gest_cargo.models import Cargo

# Cargo


class EleccionForm(ModelForm):
    fecha = DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Eleccion
        fields = ['titulo', 'fecha', 'cargo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['cargo'].queryset = Cargo.objects.filter(active=True)
