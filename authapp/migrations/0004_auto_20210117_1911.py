# Generated by Django 2.2.17 on 2021-01-17 16:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210117_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 19, 16, 11, 46, 148420, tzinfo=utc)),
        ),
    ]
