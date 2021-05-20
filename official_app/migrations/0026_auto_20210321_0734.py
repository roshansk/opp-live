# Generated by Django 3.1.4 on 2021-03-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_app', '0025_auto_20210304_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='nid',
            field=models.TextField(default='05A61A', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offence',
            name='id',
            field=models.TextField(default='642781', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='offender',
            name='face_img',
            field=models.ImageField(default='user-regular.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='offender',
            name='id',
            field=models.TextField(default='69C53F', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='station',
            name='sid',
            field=models.TextField(default='97F5416D', primary_key=True, serialize=False),
        ),
    ]
