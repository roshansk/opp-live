# Generated by Django 3.1.4 on 2021-05-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0057_auto_20210516_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='6843E4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='id',
            field=models.TextField(default='475689', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='ED9BC6', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='079BDABC', primary_key=True, serialize=False),
        ),
    ]
