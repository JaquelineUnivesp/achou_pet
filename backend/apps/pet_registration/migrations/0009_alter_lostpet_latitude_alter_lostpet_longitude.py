# Generated by Django 5.1.6 on 2025-03-19 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_registration', '0008_alter_lostpet_latitude_alter_lostpet_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostpet',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='lostpet',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True, verbose_name='Longitude'),
        ),
    ]
