# Generated by Django 3.1.4 on 2020-12-29 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_auth', '0002_auto_20201228_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='official',
            name='password',
            field=models.TextField(default=''),
        ),
    ]
