# Generated by Django 5.0.6 on 2024-06-18 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_chatgroup_groupmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmessage',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmessage',
            name='author',
        ),
        migrations.DeleteModel(
            name='ChatGroup',
        ),
        migrations.DeleteModel(
            name='GroupMessage',
        ),
    ]
