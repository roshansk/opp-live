# Generated by Django 3.1.4 on 2021-02-15 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0016_auto_20210213_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='AF69C7', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='accused_id',
            field=models.TextField(blank=True, default='413815', null=True),
        ),
        migrations.AlterField(
            model_name='offence',
            name='offence_id',
            field=models.TextField(default='BAE8BC2E', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='2B4BD5', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='132C0CF7', primary_key=True, serialize=False),
        ),
    ]
