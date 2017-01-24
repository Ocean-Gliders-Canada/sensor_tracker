# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-24 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the institution', max_length=300)),
                ('url', models.CharField(help_text="The institution's URL", max_length=1000)),
                ('street', models.TextField(max_length=255)),
                ('city', models.CharField(max_length=40)),
                ('province', models.CharField(max_length=80)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=80)),
                ('contact_name', models.CharField(blank=True, max_length=70, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('street', models.TextField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=40, null=True)),
                ('province', models.CharField(blank=True, max_length=80, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=80, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=70, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='<b>Example:</b> Collaborative Operations with Mote Marine Laboratory', max_length=1000)),
            ],
        ),
    ]
