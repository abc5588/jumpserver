# Generated by Django 3.2.14 on 2023-02-21 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0109_alter_asset_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ['name'], 'permissions': [('refresh_assethardwareinfo', 'Can refresh asset hardware info'), ('test_assetconnectivity', 'Can test asset connectivity'), ('match_asset', 'Can match asset'), ('change_assetnodes', 'Can change asset nodes')], 'verbose_name': 'Asset'},
        ),
    ]
