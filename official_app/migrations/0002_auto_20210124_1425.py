# Generated by Django 3.1.4 on 2021-01-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offence',
            name='accused_contact_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='offence',
            name='applicant_contact_number',
            field=models.IntegerField(),
        ),
    ]
