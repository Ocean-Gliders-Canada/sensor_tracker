# Generated by Django 2.2.4 on 2019-09-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0007_auto_20190918_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformdeployment',
            name='sea_name',
            field=models.CharField(help_text="The sea in which the study is being conducted: <a href='https://www.nodc.noaa.gov/General/NODC-Archive/seanamelist.txt'>Sea Names</a>", max_length=300),
        ),
    ]
