# Generated by Django 2.2.1 on 2019-05-24 09:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20190521_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
