# Generated by Django 5.1.1 on 2024-11-02 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_city_arrival_passenger_cityarrival_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='countryDepartue',
            new_name='countryDeparture',
        ),
    ]
