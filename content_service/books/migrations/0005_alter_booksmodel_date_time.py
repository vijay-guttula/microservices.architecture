# Generated by Django 4.0 on 2022-01-03 09:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_booksmodel_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksmodel',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 3, 9, 53, 52, 416316, tzinfo=utc)),
        ),
    ]
