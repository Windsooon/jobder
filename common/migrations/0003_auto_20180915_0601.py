# Generated by Django 2.0 on 2018-09-15 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20180915_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='common.Settings'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='stripe_last4',
            field=models.CharField(blank=True, default='2345', max_length=48),
            preserve_default=False,
        ),
    ]
