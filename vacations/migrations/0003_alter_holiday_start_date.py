# Generated by Django 4.2.9 on 2024-01-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0002_remove_location_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='start_date',
            field=models.CharField(max_length=200),
        ),
    ]