# Generated by Django 4.2.9 on 2024-01-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0006_rename_free_slots_holiday_freeslots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='startDate',
            field=models.CharField(max_length=50),
        ),
    ]
