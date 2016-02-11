from django.db import models
from django.shortcuts import resolve_url


class Speaker(models.Model):

    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descrição', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve_url('speaker_detail', slug=self.slug)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'


class Contact(models.Model):

    EMAIL = 'E'
    TELEPHONE = 'T'
    KINDS = ((EMAIL, 'E-mail'), (TELEPHONE, 'Telefone'))

    speaker = models.ForeignKey('Speaker', verbose_name='palestrante')
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('contato', max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
