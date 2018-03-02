# Generated by Django 2.0.1 on 2018-02-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20180205_1219'),
        ('common', '0004_auto_20180205_0551'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=256)),
                ('avatar_url', models.CharField(blank=True, max_length=256)),
                ('repo', models.ManyToManyField(to='post.Repo')),
            ],
        ),
    ]
