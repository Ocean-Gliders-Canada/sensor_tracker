# Generated by Django 2.2.6 on 2019-11-07 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0014_auto_20190620_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='instrument',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='instruments.Instrument'),
        ),
    ]
