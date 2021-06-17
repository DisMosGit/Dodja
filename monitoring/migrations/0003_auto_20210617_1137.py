# Generated by Django 3.2.4 on 2021-06-17 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_auto_20210616_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoring',
            name='next_launch',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='next_launch'),
        ),
        migrations.AlterField(
            model_name='monitoring',
            name='priority',
            field=models.IntegerField(default=0, verbose_name='priority'),
        ),
    ]