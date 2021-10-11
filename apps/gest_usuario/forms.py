from django import forms
from django.core.exceptions import ValidationError


class ClaveForm(forms.Form):
    # clave = forms.CharField(label='Clave de 8 caracteres', max_length=8)
    clave = forms.CharField(label='Clave de 8 caracteres',
                            min_length=8,
                            max_length=16,
                            widget=forms.PasswordInput)
    repetir_clave = forms.CharField(label='Repita la clave',
                                    min_length=8,
                                    max_length=16,
                                    widget=forms.PasswordInput)

    class Meta:
        fields = ['clave', 'repetir_clave', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get('clave')
        repetir_clave = cleaned_data.get('repetir_clave')
        if clave and repetir_clave:
            if clave != repetir_clave:
                raise ValidationError({
                    'repetir_clave': ValidationError('LAS CLAVES SON DISTINTAS')})
