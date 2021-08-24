# Generated by Django 3.1.12 on 2021-08-23 07:52

from django.db import migrations


def init_user_msg_subscription(apps, schema_editor):
    UserMsgSubscription = apps.get_model('notifications', 'UserMsgSubscription')
    User = apps.get_model('users', 'User')

    to_create = []
    users = User.objects.all()
    for user in users:
        receive_backends = []

        receive_backends.append('site_msg')

        if user.email:
            receive_backends.append('email')

        if user.wecom_id:
            receive_backends.append('wecom')

        if user.dingtalk_id:
            receive_backends.append('dingtalk')

        if user.feishu_id:
            receive_backends.append('feishu')

        to_create.append(UserMsgSubscription(user=user, receive_backends=receive_backends))
    UserMsgSubscription.objects.bulk_create(to_create)
    print(f'\n  Init user message subscription: {len(to_create)}')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_user_feishu_id'),
        ('notifications', '0002_auto_20210823_1619'),
    ]

    operations = [
        migrations.RunPython(init_user_msg_subscription)
    ]
