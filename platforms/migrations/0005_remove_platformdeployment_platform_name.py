# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-06-19 15:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0004_deactivate_platforms_vr3_vr4'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformdeployment',
            name='platform_name',
        ),
    ]
