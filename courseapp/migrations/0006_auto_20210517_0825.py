# Generated by Django 2.2 on 2021-05-17 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0005_course_expiry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='created_by',
            new_name='user',
        ),
    ]