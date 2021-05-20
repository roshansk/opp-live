# Generated by Django 3.1.4 on 2021-05-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0049_auto_20210512_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='116E4D', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='id',
            field=models.TextField(default='99F580', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='8E6D19', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='8253CAC5', primary_key=True, serialize=False),
        ),
    ]
