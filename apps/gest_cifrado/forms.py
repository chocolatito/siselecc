from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

VALIDATOR = [RegexValidator('^[a-zA-Z0-9|ñ|Ñ|.|,|_|-|$|@]{8}$',
                            message='Caracteres no permitidos',
                            code='formato_incorrecto'), ]

COLORES = [
    (23, 'Verde'),
    (13, 'Azul'),
    (12, 'Rojo'),
]


class ClaveForm(forms.Form):
    # clave = forms.CharField(label='Clave de 8 caracteres', max_length=8)
    clave = forms.CharField(label='Clave de 8 caracteres',
                            max_length=8,
                            validators=VALIDATOR,
                            widget=forms.PasswordInput)
    repetir_clave = forms.CharField(label='Repita la clave',
                                    max_length=8,
                                    widget=forms.PasswordInput)
    color = forms.CharField(label='Seleccione el color',
                            widget=forms.Select(choices=COLORES))

    class Meta:
        fields = ['clave', 'repetir_clave', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    def algo_pasa(self):
        print(3*'\n'+"ALGO ESTA PASANDO3"+'\n'*3)

    def clean_clave(self):
        clave = self.cleaned_data.get('clave')
        if clave:
            return clave
        else:
            raise ValidationError('Clave mal')

    def clean_repetir_clave(self):
        repetir_clave = self.cleaned_data.get('repetir_clave')
        if repetir_clave:
            return repetir_clave
        else:
            raise ValidationError('Clave mal')

    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get('clave')
        repetir_clave = cleaned_data.get('repetir_clave')
        if clave and repetir_clave:
            if clave != repetir_clave:
                raise ValidationError({
                    'repetir_clave': ValidationError('LAS CLAVES SON DISTINTAS')})
