# Generated by Django 4.0 on 2022-01-03 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksmodel',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 3, 9, 46, 39, 883296)),
        ),
    ]