from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Cargo

# Cargo


class CargoForm(ModelForm):

    class Meta:
        model = Cargo
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if self.instance.pk:
            if Cargo.objects.exclude(pk=self.instance.pk).filter(nombre__iexact=nombre):
                raise ValidationError('YA EXISTE UN CARGO REGISTRADO CON ESE NOMBRE')
            else:
                return nombre
        else:
            if Cargo.objects.filter(nombre__iexact=nombre):
                raise ValidationError('YA EXISTE UN CARGO REGISTRADO CON ESE NOMBRE')
            else:
                return nombre
