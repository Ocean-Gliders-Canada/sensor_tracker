# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-24 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the platform', max_length=300)),
                ('wmo_id', models.IntegerField(blank=True, help_text="The WMO ID for the mission. See: <a href='http://www.jcomm.info/index.php?option=com_oe&task=viewGroupRecord&groupID=155'>WMO Contact Info</a> to acquire", null=True)),
                ('serial_number', models.CharField(max_length=300)),
                ('purchase_date', models.DateTimeField(blank=True, null=True)),
                ('institution', models.ForeignKey(help_text='The institution who owns the platform', on_delete=django.db.models.deletion.CASCADE, to='general.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='This is a good place to log any problems or changes with a platform')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformDeployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wmo_id', models.IntegerField(blank=True, help_text="The WMO ID for the mission. See: <a href='http://www.jcomm.info/index.php?option=com_oe&task=viewGroupRecord&groupID=155'>WMO Contact Info</a> to acquire", null=True)),
                ('deployment_number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(help_text='A short descriptive title for the deployment.', max_length=500)),
                ('start_time', models.DateTimeField()),
                ('deployment_name', models.CharField(max_length=150)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('acknowledgement', models.CharField(blank=True, help_text='<b>Example:</b> This deployment is supported by funding from NOAA', max_length=900, null=True)),
                ('contributor_name', models.TextField(blank=True, help_text='A comma separated list of contributors to this data set<br><b>Example:</b> "Jerry Garcia, Bob Weir, Bill Graham"', null=True)),
                ('contributor_role', models.TextField(blank=True, help_text='A comma separated list of the roles for those specified in the contributor_name attribute<br><b>Example:</b> "Principal Investigator, Principal Investigator, Data Manager"', null=True)),
                ('creator_email', models.CharField(blank=True, help_text='Email address for the person who collected the data.', max_length=150, null=True)),
                ('creator_name', models.CharField(blank=True, help_text='Name of the person who collected the data.', max_length=150, null=True)),
                ('creator_url', models.CharField(blank=True, help_text='URL for the person who collected the data.', max_length=150, null=True)),
                ('sea_name', models.CharField(default='North Atlantic Ocean', help_text="The sea in which the study is being conducted: <a href='https://www.nodc.noaa.gov/General/NODC-Archive/seanamelist.txt'>Sea Names</a>", max_length=300)),
                ('institution', models.ForeignKey(help_text='The institution responsible for the deployment.', on_delete=django.db.models.deletion.PROTECT, to='general.Institution')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.Platform')),
                ('project', models.ForeignKey(help_text='The project the data is being collected under.', on_delete=django.db.models.deletion.PROTECT, to='general.Project')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformDeploymentComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='This is a good place to log any changes to a deployment')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('platform_deployment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.PlatformDeployment')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=300)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Manufacturer')),
            ],
        ),
        migrations.AddField(
            model_name='platform',
            name='platform_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.PlatformType'),
        ),
    ]