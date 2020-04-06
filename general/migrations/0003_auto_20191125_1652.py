# Generated by Django 2.2.6 on 2019-11-25 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_auto_20190611_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='country',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='province',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='street',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
