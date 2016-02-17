from django.test import TestCase
from django.shortcuts import resolve_url
from eventex.core.models import Speaker, Talk


class TalkListGet(TestCase):

    def setUp(self):
        talk1 = Talk.objects.create(title='Título da Palestra', start='10:00',
                                    description='Lorem ipsum')
        talk2 = Talk.objects.create(title='Título da Palestra', start='13:00',
                                    description='Lorem ipsum')
        speaker = Speaker.objects.create(name='Nome do Palestrante',
                                         slug='nome-do-palestrante',
                                         website='http://palestrant.es/ndp/')
        talk1.speakers.add(speaker)
        talk2.speakers.add(speaker)
        self.resp = self.client.get(resolve_url('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talk_list.html')

    def test_html(self):
        contents = [(2, 'Título da Palestra'),
                    (1, '10:00'),
                    (1, '13:00'),
                    (2, '/palestrantes/nome-do-palestrante/'),
                    (2, 'Nome do Palestrante'),
                    (2, 'Lorem ipsum')]
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_context(self):
        variables = ['morning_talks', 'afternoon_talks']
        for key in variables:
            with self.subTest():
                self.assertIn(key, self.resp.context)


class TalkListGetEmpty(TestCase):

    def test_get_empty(self):
        resp = self.client.get(resolve_url('talk_list'))
        contents = ('manhã', 'tarde')
        for expected in contents:
            with self.subTest():
                phrase =  'Ainda não existem palestras confirmadas de {}'.format(expected)
                self.assertContains(resp, phrase)