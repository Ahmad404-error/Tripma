# Generated by Django 5.1 on 2024-09-18 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airport',
            old_name='longitide',
            new_name='longitude',
        ),
    ]
