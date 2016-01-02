from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')
        self.form = self.response.context['form']

    def test_get(self):
        """ GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response,
                                'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain CSRF"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        self.assertSequenceEqual(list(self.form.fields),
                                 ['name', 'cpf', 'email', 'phone'])


class SubscribePostTest(TestCase):

    def setUp(self):
        data = {'name': 'John Due',
                'cpf': '12345678900',
                'email': 'email@server.com',
                'phone': '42'}
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid post should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        self.assertEqual('Confirmação de Inscrição',
                         self.email.subject)

    def test_subscription_email_from(self):
        self.assertEqual('contato@eventex.com.br', self.email.from_email)

    def test_subscription_email_to(self):
        self.assertEqual(['contato@eventex.com.br', 'email@server.com'],
                         self.email.to)

    def test_subscription_email_body(self):
        self.assertIn('John Due', self.email.body)
        self.assertIn('12345678900', self.email.body)
        self.assertIn('email@server.com', self.email.body)
        self.assertIn('42', self.email.body)


class SubscribeInvalidPostTest(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', dict())
        self.form = self.response.context['form']

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response,
                                'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_has_errors(self):
        self.assertTrue(self.form.errors)


class SubscribeSUccessMessage(TestCase):

    def test_message(self):
        data = {'name': 'John Due',
                'cpf': '12345678900',
                'email': 'email@server.com',
                'phone': '42'}
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
