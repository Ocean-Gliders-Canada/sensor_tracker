# Generated by Django 2.2.8 on 2020-02-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0015_auto_20200224_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformpowertype',
            name='name',
            field=models.CharField(help_text='Power source of this deployment', max_length=500, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='platform',
            unique_together={('name', 'serial_number')},
        ),
    ]
