# Generated by Django 3.2.4 on 2021-06-19 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_auto_20210619_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='htmlnotification',
            name='host',
        ),
    ]