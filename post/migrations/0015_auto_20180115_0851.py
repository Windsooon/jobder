# Generated by Django 2.0 on 2018-01-15 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_auto_20180115_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pay_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 15, 8, 51, 19, 63533, tzinfo=utc)),
        ),
    ]