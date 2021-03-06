# Generated by Django 3.0.8 on 2020-07-24 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0010_auto_20200722_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Bussiness_Type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='Business_Type',
            field=models.CharField(choices=[('test1', 'test1'), ('test2', 'test2'), ('test3', 'test3'), ('test4', 'test4')], default='test1', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='business_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='discount_provided',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='profile',
            name='partner_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='@gmail.com', max_length=254),
        ),
    ]
