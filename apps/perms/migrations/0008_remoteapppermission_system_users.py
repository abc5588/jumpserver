# Generated by Django 2.1.7 on 2019-09-09 09:09

from django.db import migrations, models
from assets.models import SystemUser


def migrate_system_user_from_remote_app_to_remote_app_perms(apps, schema_editor):
    remote_app_perms_model = apps.get_model("perms", "RemoteAppPermission")
    db_alias = schema_editor.connection.alias
    perms = remote_app_perms_model.objects.using(db_alias).all()
    for perm in perms:
        system_user_ids = perm.remote_apps.values_list('system_user', flat=True)
        perm.system_users.set(system_user_ids)


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0037_auto_20190724_2002'),
        ('perms', '0007_remove_assetpermission_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='remoteapppermission',
            name='system_users',
            field=models.ManyToManyField(related_name='granted_by_remote_app_permissions', to='assets.SystemUser', verbose_name='System user'),
        ),
        migrations.RunPython(
            code=migrate_system_user_from_remote_app_to_remote_app_perms,
        ),
    ]
