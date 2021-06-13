from django.forms import ModelForm
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
    def save(self, commit=True):
        object = super().save(commit=False)
        print(f'\nEl nuevo objeto:\t{object.dni}')
        if commit:
            object.save()
        return object
"""
