# Generated by Django 3.0.3 on 2020-02-26 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200220_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpage',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Post date'),
        ),
    ]