# Generated by Django 2.2.6 on 2019-11-20 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0009_merge_20191106_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformdeployment',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.Platform'),
        ),
    ]
