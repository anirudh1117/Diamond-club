# Generated by Django 3.0.8 on 2020-07-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0007_auto_20200720_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Bussiness_Type',
            field=models.CharField(choices=[('a', 'test1'), ('b', 'test2'), ('c', 'test3'), ('d', 'test4')], default='test1', max_length=20),
        ),
    ]
