# Generated by Django 3.0.8 on 2020-07-14 19:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0003_auto_20200715_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
