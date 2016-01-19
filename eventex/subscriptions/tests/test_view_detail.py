from django.shortcuts import resolve_url
from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):

    def setUp(self):
        self.obj = Subscription.objects.create(name='Harry Potter',
                                               email='harrypotter@mailinator.com',
                                               phone='2345678',
                                               cpf='12345678900')
        self.resp = self.client.get(resolve_url('subscriptions:detail', self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        data = (self.obj.name, self.obj.email, self.obj.phone, self.obj.cpf)
        with self.subTest():
            for expected in data:
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('subscriptions:detail', 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
