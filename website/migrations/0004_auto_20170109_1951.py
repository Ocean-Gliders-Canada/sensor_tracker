# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-09 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20170109_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='contact_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='contact_name',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
