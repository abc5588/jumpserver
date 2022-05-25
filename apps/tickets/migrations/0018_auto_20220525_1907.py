# Generated by Django 3.1.14 on 2022-05-25 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_applytickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketstep',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('pending', 'Pending')], default='pending', max_length=16),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('open', 'Open'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('closed', 'Closed')], default='pending', max_length=16, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='ticketassignee',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('notified', 'Notified'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='notified', max_length=64),
        ),
        migrations.AlterField(
            model_name='ticketstep',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('notified', 'Notified'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=64),
        ),
    ]
