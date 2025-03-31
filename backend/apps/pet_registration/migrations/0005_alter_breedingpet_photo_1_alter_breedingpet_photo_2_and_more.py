# Generated by Django 5.1.6 on 2025-03-18 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_registration', '0004_breedingpet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breedingpet',
            name='photo_1',
            field=models.ImageField(blank=True, null=True, upload_to='breeding_pets/'),
        ),
        migrations.AlterField(
            model_name='breedingpet',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to='breeding_pets/'),
        ),
        migrations.AlterField(
            model_name='breedingpet',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to='breeding_pets/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_1',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_pets/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_pets/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_pets/'),
        ),
    ]
