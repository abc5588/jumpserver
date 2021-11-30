# Generated by Django 3.1.13 on 2021-11-30 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_auto_20210812_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('date_created',), 'verbose_name': 'Comment'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ('-date_created',), 'verbose_name': 'Ticket'},
        ),
        migrations.AlterModelOptions(
            name='ticketstep',
            options={'verbose_name': 'Ticket step'},
        ),
    ]
