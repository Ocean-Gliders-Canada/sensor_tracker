# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-06-17 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instruments', '0003_auto_20190611_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentCommentBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument',
                 models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='instruments.Instrument')),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentCommentInBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Comments')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('instrument_comment_box',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instruments.InstrumentCommentBox')),
                ('user', models.ForeignKey( null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
