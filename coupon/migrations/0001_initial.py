# Generated by Django 3.0.8 on 2020-08-02 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllCoupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_Number', models.PositiveIntegerField()),
                ('coupon_valid', models.DateTimeField()),
            ],
        ),
    ]