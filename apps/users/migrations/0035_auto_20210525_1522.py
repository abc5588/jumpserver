# Generated by Django 3.1 on 2021-05-25 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20210506_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='need_update_password',
            field=models.BooleanField(default=False, verbose_name='Need update password'),
        ),
    ]
