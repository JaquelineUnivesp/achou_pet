# Generated by Django 5.1.6 on 2025-03-06 21:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_registration', '0002_petadoption'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='petadoption',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adoption_pets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_1',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_photos/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_photos/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to='adoption_photos/'),
        ),
        migrations.AlterField(
            model_name='petadoption',
            name='status',
            field=models.CharField(default='adoption', editable=False, max_length=20),
        ),
    ]
