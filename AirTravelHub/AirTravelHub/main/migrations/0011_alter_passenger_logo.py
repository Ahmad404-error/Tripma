# Generated by Django 5.1.1 on 2024-10-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_passenger_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='logo',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]