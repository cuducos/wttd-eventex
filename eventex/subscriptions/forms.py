from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números.', 'digits')
    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.', 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.CharField(label='Telefone', required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        words = [word.capitalize() for word in name.split()]
        return ' '.join(words)

    def clean(self):
        if not any([self.cleaned_data.get('email'), self.cleaned_data.get('phone')]):
            raise ValidationError('Informe seu email ou telefone', 'contact')
        return self.cleaned_data
