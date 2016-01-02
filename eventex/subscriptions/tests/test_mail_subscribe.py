from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):

    def setUp(self):
        self.client.post('/inscricao/', dict(name='John Due',
                                             cpf='12345678900',
                                             email='email@server.com',
                                             phone='42'))
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        self.assertEqual('Confirmação de Inscrição',
                         self.email.subject)

    def test_subscription_email_from(self):
        self.assertEqual('contato@eventex.com.br', self.email.from_email)

    def test_subscription_email_to(self):
        self.assertEqual(['contato@eventex.com.br', 'email@server.com'],
                         self.email.to)

    def test_subscription_email_body(self):
        contents = ['John Due', '12345678900', 'email@server.com', '42']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
