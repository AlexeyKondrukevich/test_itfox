# Generated by Django 4.2.2 on 2023-08-17 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]