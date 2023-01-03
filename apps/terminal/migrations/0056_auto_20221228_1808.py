# Generated by Django 3.2.14 on 2022-12-28 10:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('assets', '0105_auto_20221220_1956'),
        ('terminal', '0055_auto_20221228_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applet',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.SlugField(max_length=128, unique=True, verbose_name='Name')),
                ('display_name', models.CharField(max_length=128, verbose_name='Display name')),
                ('version', models.CharField(max_length=16, verbose_name='Version')),
                ('author', models.CharField(max_length=128, verbose_name='Author')),
                ('type',
                 models.CharField(choices=[('general', 'General'), ('web', 'Web')], default='general', max_length=16,
                                  verbose_name='Type')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('builtin', models.BooleanField(default=False, verbose_name='Builtin')),
                ('protocols', models.JSONField(default=list, verbose_name='Protocol')),
                ('tags', models.JSONField(default=list, verbose_name='Tags')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'Applet',
            },
        ),
        migrations.CreateModel(
            name='AppletHost',
            fields=[
                ('host_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='assets.host')),
                ('deploy_options', models.JSONField(default=dict, verbose_name='Deploy options')),
                ('inited', models.BooleanField(default=False, verbose_name='Inited')),
                ('date_inited', models.DateTimeField(blank=True, null=True, verbose_name='Date inited')),
                ('date_synced', models.DateTimeField(blank=True, null=True, verbose_name='Date synced')),
            ],
            options={
                'verbose_name': 'Applet host',
            },
            bases=('assets.host',),
        ),
        migrations.CreateModel(
            name='AppletPublication',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status', models.CharField(default='ready', max_length=16, verbose_name='Status')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('applet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='publications',
                                             to='terminal.applet', verbose_name='Applet')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='publications',
                                           to='terminal.applethost', verbose_name='Host')),
            ],
            options={
                'unique_together': {('applet', 'host')},
            },
        ),
        migrations.CreateModel(
            name='AppletHostDeployment',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('initial', models.BooleanField(default=False, verbose_name='Initial')),
                ('status', models.CharField(default='', max_length=16, verbose_name='Status')),
                ('date_start', models.DateTimeField(db_index=True, null=True, verbose_name='Date start')),
                ('date_finished', models.DateTimeField(null=True, verbose_name='Date finished')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('task', models.UUIDField(null=True, verbose_name='Task')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terminal.applethost',
                                           verbose_name='Hosting')),
            ],
            options={
                'ordering': ('-date_start',),
            },
        ),
        migrations.AddField(
            model_name='applethost',
            name='applets',
            field=models.ManyToManyField(through='terminal.AppletPublication', to='terminal.Applet',
                                         verbose_name='Applet'),
        ),
        migrations.AddField(
            model_name='applethost',
            name='terminal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                       related_name='applet_host', to='terminal.terminal', verbose_name='Terminal'),
        ),
        migrations.AddField(
            model_name='applet',
            name='hosts',
            field=models.ManyToManyField(through='terminal.AppletPublication', to='terminal.AppletHost',
                                         verbose_name='Hosts'),
        ),
    ]
