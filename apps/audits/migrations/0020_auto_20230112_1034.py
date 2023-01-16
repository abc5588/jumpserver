# Generated by Django 3.2.14 on 2023-01-12 02:34

import common.db.encoder
from django.db import migrations, models

from audits.handler import OperatorLogHandler


def migrate_operate_log_after_before(apps, schema_editor):
    operate_log_model = apps.get_model("audits", "OperateLog")
    db_alias = schema_editor.connection.alias
    queryset = operate_log_model.objects.using(db_alias).all()
    operate_logs = []
    for inst in queryset:
        before, after, diff = inst.before, inst.after, dict()
        if not any([before, after]):
            continue
        operator = OperatorLogHandler()
        diff = operator.convert_before_after_to_diff(before, after)
        inst.diff = diff
        operate_logs.append(inst)
    operate_log_model.objects.bulk_update(operate_logs, ['diff'])


class Migration(migrations.Migration):

    dependencies = [
        ('audits', '0019_alter_operatelog_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='operatelog',
            name='diff',
            field=models.JSONField(default=dict, encoder=common.db.encoder.ModelJSONFieldEncoder, null=True),
        ),
        migrations.AddField(
            model_name='operatelog',
            name='detail',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Detail'),
        ),
        migrations.RunPython(migrate_operate_log_after_before),
        migrations.RemoveField(model_name='operatelog', name='after',),
        migrations.RemoveField(model_name='operatelog', name='before',),
    ]
