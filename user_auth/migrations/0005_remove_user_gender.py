# Generated by Django 3.1.4 on 2021-01-27 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
