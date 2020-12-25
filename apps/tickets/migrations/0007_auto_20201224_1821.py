# Generated by Django 3.1 on 2020-12-24 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tickets.models.ticket

TICKET_TYPE_APPLY_ASSET = 'apply_asset'


def migrate_field_type(tp):
    if tp == 'request_asset':
        return TICKET_TYPE_APPLY_ASSET
    return tp


def migrate_field_meta(tp, old_meta):
    if tp != TICKET_TYPE_APPLY_ASSET or not old_meta:
        return old_meta
    old_meta_hostname = old_meta.get('hostname')
    old_meta_system_user = old_meta.get('system_user')
    new_meta = {
        'apply_ip_group': old_meta.get('ips', []),
        'apply_hostname_group': [old_meta_hostname] if old_meta_hostname else [],
        'apply_system_user_group': [old_meta_system_user] if old_meta_system_user else [],
        'apply_actions': old_meta.get('actions'),
        'apply_date_start': old_meta.get('date_start'),
        'apply_date_expired': old_meta.get('date_expired'),

        'approve_assets': old_meta.get('confirmed_assets', []),
        'approve_system_users': old_meta.get('confirmed_system_users', []),
        'approve_actions': old_meta.get('actions'),
        'approve_date_start': old_meta.get('date_start'),
        'approve_date_expired': old_meta.get('date_expired'),
    }
    return new_meta


def migrate_tickets_fields_name(apps, schema_editor):
    ticket_model = apps.get_model("tickets", "Ticket")
    tickets = ticket_model.origin_objects.all()

    for ticket in tickets:
        ticket.applicant = ticket.user
        ticket.applicant_display = ticket.user_display
        ticket.processor = ticket.assignee
        ticket.processor_display = ticket.assignee_display
        ticket.type = migrate_field_type(ticket.type)
        ticket.meta = migrate_field_meta(ticket.type, ticket.meta)
        ticket.meta['body'] = ticket.body
        ticket.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0006_auto_20201023_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='applicant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applied_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Applicant'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='applicant_display',
            field=models.CharField(default='', max_length=128, verbose_name='Applicant display'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Processor'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='processor_display',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Processor display'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assignees',
            field=models.ManyToManyField(related_name='assigned_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Assignees'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assignees_display',
            field=models.CharField(blank=True, max_length=128, verbose_name='Assignees display'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='meta',
            field=models.JSONField(encoder=tickets.models.ticket.ModelJSONFieldEncoder, verbose_name='Meta'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('general', 'General'), ('login_confirm', 'Login confirm'), ('apply_asset', 'Apply for asset'), ('apply_application', 'Apply for application')], default='general', max_length=64, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='action',
            field=models.CharField(blank=True, choices=[('approve', 'Approve'), ('reject', 'Reject')], default='', max_length=16, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=16, verbose_name='Status'),
        ),
        migrations.RunPython(migrate_tickets_fields_name),
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='user_display',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='assignee_display',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='body',
        ),
        migrations.AlterModelManagers(
            name='ticket',
            managers=[
            ],
        ),
    ]
