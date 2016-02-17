from django.db import models
from django.shortcuts import resolve_url

from eventex.core.managers import KindQuerySet, PeriodManager


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

    objects = KindQuerySet.as_manager()

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'


class Talk(models.Model):

    title = models.CharField('título', max_length=255)
    start = models.TimeField('início', blank=True, null=True)
    description = models.TextField('descrição', blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='palestrante',
                                      blank=True)

    objects = PeriodManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'palestra'
        verbose_name_plural = 'palestras'
