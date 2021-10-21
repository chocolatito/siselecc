from django.forms import DateField, ModelChoiceField, NumberInput, HiddenInput
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Eleccion
from ..gest_cargo.models import Cargo

# Cargo


class EleccionForm(ModelForm):
    fecha = DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Eleccion
        fields = ['titulo', 'fecha', 'cargo', 'staff']

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/questions/7299973/django-how-to-access-current-request-user-in-modelform
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
            kwargs['initial']={'staff':self.user}
        super().__init__(*args, **kwargs)
        self.fields['staff'].widget=HiddenInput()

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['cargo'].queryset = Cargo.objects.filter(active=True)
        print(self.fields['staff'].widget.attrs)
        print(self.fields['staff'].widget)




class EleccionUpdateForm(ModelForm):
    fecha = DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Eleccion
        fields = ['titulo', 'fecha',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        # self.fields['cargo'].queryset = Cargo.objects.filter(active=True)
