from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormtest(TestCase):

    def setUp(self):
        self.form = SubscriptionForm()

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        self.assertSequenceEqual(list(self.form.fields),
                                 ['name', 'cpf', 'email', 'phone'])
