from django.forms import ModelForm
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
