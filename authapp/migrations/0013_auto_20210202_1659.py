# Generated by Django 3.1.5 on 2021-02-02 13:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_auto_20210202_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 4, 13, 59, 19, 924824, tzinfo=utc)),
        ),
    ]
