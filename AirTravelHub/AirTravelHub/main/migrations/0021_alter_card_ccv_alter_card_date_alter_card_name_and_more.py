# Generated by Django 5.1.1 on 2024-11-03 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_card_date_alter_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='ccv',
            field=models.CharField(default='None', max_length=3),
        ),
        migrations.AlterField(
            model_name='card',
            name='date',
            field=models.CharField(default='None', max_length=5),
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(default='None', max_length=16),
        ),
    ]