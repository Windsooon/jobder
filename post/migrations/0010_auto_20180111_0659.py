# Generated by Django 2.0 on 2018-01-11 06:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20180110_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 6, 59, 35, 948357, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='pay_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 6, 59, 35, 948322, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 6, 59, 35, 948376, tzinfo=utc)),
        ),
    ]