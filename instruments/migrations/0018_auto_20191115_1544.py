# Generated by Django 2.2.6 on 2019-11-15 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0017_auto_20191108_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensoroninstrument',
            options={'verbose_name': 'Sensor on Instrument History', 'verbose_name_plural': 'Sensor on Instrument Histories'},
        ),
    ]