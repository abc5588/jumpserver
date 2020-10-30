# Generated by Django 2.2.13 on 2020-10-26 11:31

from django.db import migrations, models


def get_node_ancestor_keys(key, with_self=False):
    parent_keys = []
    key_list = key.split(":")
    if not with_self:
        key_list.pop()
    for i in range(len(key_list)):
        parent_keys.append(":".join(key_list))
        key_list.pop()
    return parent_keys


def migrate_nodes_value_with_slash(apps, schema_editor):
    model = apps.get_model("assets", "Node")
    db_alias = schema_editor.connection.alias
    nodes = model.objects.using(db_alias).filter(value__contains='/')
    print('')
    print("- Start migrate node value if has /")
    for i, node in enumerate(list(nodes)):
        new_value = node.value.replace('/', '|')
        print("{} start migrate node value: {} => {}".format(i, node.value, new_value))
        node.value = new_value
        node.save()


def migrate_nodes_full_value(apps, schema_editor):
    model = apps.get_model("assets", "Node")
    db_alias = schema_editor.connection.alias
    nodes = model.objects.using(db_alias).all()
    print("- Start migrate node full value")
    for i, node in enumerate(list(nodes)):
        print("{} start migrate {} node full value".format(i, node.value))
        ancestor_keys = get_node_ancestor_keys(node.key, True)
        values = model.objects.filter(key__in=ancestor_keys).values_list('key', 'value')
        values = [v for k, v in sorted(values, key=lambda x: len(x[0]))]
        node.full_value = '/'.join(values)
        node.save()


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0059_auto_20201027_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='full_value',
            field=models.CharField(default='', max_length=4096, verbose_name='Full value'),
        ),
        migrations.RunPython(migrate_nodes_value_with_slash),
        migrations.RunPython(migrate_nodes_full_value)
    ]
