from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormtest(TestCase):

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        self.assertSequenceEqual(list(form.fields),
                                 ['name', 'cpf', 'email', 'phone'])

    def test_if_cpf_is_numeric(self):
        """CPF must contain only numbers"""
        form = self.make_validated_form(cpf='ABC45678900')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must contain 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized."""
        form = self.make_validated_form(name='JOHN doe')
        self.assertEqual('John Doe', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and phone are optional, but one of them must be informed"""
        form = self.make_validated_form(phone='', email='')
        self.assertFormErrorCode(form, '__all__', 'contact')

    def make_validated_form(self, **kwargs):
        valid = dict(name='John Doe', cpf='12345678900',
                     email='johndoe@mailinator.com', phone='2345678')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        exception = errors[field][0]
        self.assertEqual(exception.code, code)
