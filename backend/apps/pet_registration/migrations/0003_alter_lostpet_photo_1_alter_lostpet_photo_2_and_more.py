# Generated by Django 5.1.6 on 2025-04-23 22:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet_registration', '0002_alter_breedingpet_breed_alter_breedingpet_coat_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostpet',
            name='photo_1',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='lostpet',
            name='photo_2',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='lostpet',
            name='photo_3',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
