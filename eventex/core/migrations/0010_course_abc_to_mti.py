# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-18 18:35
from __future__ import unicode_literals

from django.db import migrations


def move_from_source_to_target(Source, Target):
    for src in Source.objects.all():
        new = Target(title=src.title,
                     description=src.description,
                     start=src.start,
                     slots=src.slots)
        new.save()
        new.speakers.set(src.speakers.all())
        src.delete()


def forward_course_abc_to_mti(apps, schema_editor):
    move_from_source_to_target(apps.get_model('core', 'CourseOld'),
                               apps.get_model('core', 'Course'))


def backward_course_abc_to_mti(apps, schema_editor):
    move_from_source_to_target(apps.get_model('core', 'Course'),
                               apps.get_model('core', 'CourseOld'))


class Migration(migrations.Migration):

    dependencies = [('core', '0009_course'), ]

    operations = [migrations.RunPython(forward_course_abc_to_mti,
                                       backward_course_abc_to_mti)]
