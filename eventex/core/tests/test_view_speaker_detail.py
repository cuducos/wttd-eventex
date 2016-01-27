from django.test import TestCase
from django.shortcuts import resolve_url

from eventex.core.models import Speaker


class SpeakerDetailGet(TestCase):

    def setUp(self):
        Speaker.objects.create(name='Grace Hopper',
                               slug='grace-hopper',
                               website='http://hbn.link/hopper-link',
                               photo='http://hbn.link/hopper-pic',
                               description='Programadora e almirante.<br />Inventora do compilador, criadora da linguagem de programação Flow-Matic que servir de base para a linguagem COBOL permitindo a popularização das aplicações comerciais.')
        self.resp = self.client.get(resolve_url('speaker_detail', slug='grace-hopper'))

    def test_get(self):
        """GET must return status 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/speaker_detail.html')

    def test_html(self):
        contents = ['Grace Hopper',
                    'Programadora e almirante',
                    'http://hbn.link/hopper-pic',
                    'http://hbn.link/hopper-link']
        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_context(self):
        """Speaker must be in context"""
        speaker = self.resp.context['speaker']
        self.assertIsInstance(speaker, Speaker)


class SpeakerDetailNotFound(TestCase):

    def test_not_found(self):
        resp = self.client.get(resolve_url('speaker_detail', slug='john-doe'))
        self.assertEqual(404, resp.status_code)
