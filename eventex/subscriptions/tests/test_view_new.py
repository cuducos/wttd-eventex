from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeNewGet(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('subscriptions:new'))

    def test_get(self):
        """ GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """HTML must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribeNewPostValid(TestCase):

    def setUp(self):
        data = {'name': 'John Due',
                'cpf': '12345678900',
                'email': 'email@server.com',
                'phone': '42'}
        self.resp = self.client.post(resolve_url('subscriptions:new'), data)

    def test_post(self):
        """Valid post should redirect to /inscricao/<id>/"""
        self.assertRedirects(self.resp, resolve_url('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribeNewPostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(resolve_url('subscriptions:new'), dict())
        self.form = self.resp.context['form']

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_has_errors(self):
        self.assertTrue(self.form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
