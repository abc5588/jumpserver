# Generated by Django 3.2.17 on 2023-04-13 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0113_auto_20230411_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocol',
            name='public',
            field=models.BooleanField(default=True, verbose_name='Public'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='setting',
            field=models.JSONField(default=dict, verbose_name='Setting'),
        ),
    ]
