from django import forms
from django.core.exceptions import ValidationError

from eventex.subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['name', 'cpf', 'email', 'phone']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        words = [word.capitalize() for word in name.split()]
        return ' '.join(words)

    def clean(self):
        self.cleaned_data = super().clean()
        if not any([self.cleaned_data.get('email'), self.cleaned_data.get('phone')]):
            raise ValidationError('Informe seu email ou telefone', 'contact')
        return self.cleaned_data
