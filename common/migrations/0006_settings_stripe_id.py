# Generated by Django 2.0.1 on 2018-01-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_settings_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
