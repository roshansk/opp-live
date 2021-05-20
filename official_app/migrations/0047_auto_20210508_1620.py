# Generated by Django 3.1.4 on 2021-05-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0046_auto_20210508_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='offence',
            name='n_offenders',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='866959', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='id',
            field=models.TextField(default='D87CB4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='contact_number',
            field=models.CharField(blank=True, default='', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='offender',
            name='face_obj',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='470E3E', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='uid',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='8F04557A', primary_key=True, serialize=False),
        ),
    ]
