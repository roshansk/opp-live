# Generated by Django 3.1.4 on 2021-02-17 06:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0017_auto_20210215_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offence',
            old_name='gender',
            new_name='applicant_gender',
        ),
        migrations.RenameField(
            model_name='offender',
            old_name='img_obj',
            new_name='face_id_obj',
        ),
        migrations.RenameField(
            model_name='offender',
            old_name='profile_image',
            new_name='portrait_img',
        ),
        migrations.RemoveField(
            model_name='offence',
            name='accused_id',
        ),
        migrations.RemoveField(
            model_name='offence',
            name='applicant_id',
        ),
        migrations.RemoveField(
            model_name='offence',
            name='registration_date_time',
        ),
        migrations.RemoveField(
            model_name='offence',
            name='station_id',
        ),
        migrations.RemoveField(
            model_name='offender',
            name='offender_uid',
        ),
        migrations.AddField(
            model_name='offence',
            name='applicant_uid',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offence',
            name='offence_reg_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offence',
            name='status',
            field=models.TextField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='OPEN'),
        ),
        migrations.AddField(
            model_name='offence',
            name='suspect_id',
            field=models.TextField(default='Unkown', null=True),
        ),
        migrations.AddField(
            model_name='offender',
            name='contact_number',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offender',
            name='uid',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='617CAA', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='applicant_contact_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='offence',
            name='applicant_name',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='offence',
            name='offence_id',
            field=models.TextField(default='7C40C3', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='32A2E7', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='8E52067B', primary_key=True, serialize=False),
        ),
    ]
