# Generated by Django 4.1.13 on 2024-05-27 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0003_alter_user_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='verfied',
            new_name='verified',
        ),
    ]
