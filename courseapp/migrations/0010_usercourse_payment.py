# Generated by Django 2.2 on 2021-05-21 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0009_usercourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courseapp.PaymentDetails'),
        ),
    ]
