# Generated by Django 2.0 on 2017-12-22 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.URLField(blank=True)),
                ('linkedin', models.URLField(blank=True)),
                ('visiable', models.BooleanField(default=True)),
                ('location', models.SmallIntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]