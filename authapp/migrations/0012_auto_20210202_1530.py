# Generated by Django 3.1.5 on 2021-02-02 12:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20210129_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 4, 12, 30, 30, 522000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[(None, 'Введите Ваш пол'), ('M', 'М'), ('W', 'Ж')], max_length=1, verbose_name=''),
        ),
    ]
