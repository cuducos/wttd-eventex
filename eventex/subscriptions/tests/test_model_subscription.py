from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(name='John Doe',
                                cpf='12345678900',
                                email='johndoe@mailinator.com',
                                phone='2345678')
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('John Doe', str(self.obj))

    def test_paid_default_to_false(self):
        """By default paid must be False"""
        self.assertFalse(self.obj.paid)
