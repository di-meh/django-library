# Generated by Django 3.2.17 on 2023-02-09 11:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingclubsession',
            name='users',
            field=models.ManyToManyField(help_text='Select a user for this session', to=settings.AUTH_USER_MODEL),
        ),
    ]
