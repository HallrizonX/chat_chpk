# Generated by Django 2.2.1 on 2019-05-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20190524_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='title',
            field=models.CharField(blank=True, max_length=40, verbose_name='Назва чату'),
        ),
    ]