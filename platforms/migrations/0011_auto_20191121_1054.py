# Generated by Django 2.2.6 on 2019-11-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0010_auto_20191120_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platformcommentbox',
            options={'verbose_name': 'Platform Comment Box', 'verbose_name_plural': 'Platform Comment Boxes'},
        ),
        migrations.AlterModelOptions(
            name='platformdeploymentcommentbox',
            options={'verbose_name': 'Platform Deployment Comment Box', 'verbose_name_plural': 'Platform Deployment Comment Boxes'},
        ),
    ]
