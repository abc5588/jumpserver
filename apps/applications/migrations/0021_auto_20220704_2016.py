# Generated by Django 3.2.12 on 2022-07-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0020_auto_20220316_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalaccount',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Application account', 'verbose_name_plural': 'historical Application accounts'},
        ),
        migrations.AlterField(
            model_name='historicalaccount',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
