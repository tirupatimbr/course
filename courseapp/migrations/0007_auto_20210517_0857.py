# Generated by Django 2.2 on 2021-05-17 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0006_auto_20210517_0825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='user',
            new_name='created_by',
        ),
    ]
