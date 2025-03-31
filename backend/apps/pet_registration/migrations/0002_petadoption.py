# Generated by Django 5.1.6 on 2025-03-06 00:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_registration', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PetAdoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='doacao', editable=False, max_length=20)),
                ('relationship_with_pet', models.CharField(choices=[('owner', 'Dono'), ('temporary_caretaker', 'Cuidador Temporário'), ('rescuer', 'Responsável pelo Resgate')], max_length=50)),
                ('pet_name', models.CharField(blank=True, max_length=100, null=True)),
                ('approximate_age', models.CharField(max_length=50)),
                ('is_neutered', models.CharField(choices=[('yes', 'Sim'), ('no', 'Não')], max_length=10)),
                ('approximate_weight', models.CharField(blank=True, max_length=50, null=True)),
                ('is_vaccinated', models.CharField(choices=[('yes', 'Sim'), ('no', 'Não')], max_length=10)),
                ('health_issues', models.TextField(blank=True, help_text='Problemas de saúde ou necessidades especiais', null=True)),
                ('sociable_with_animals', models.CharField(choices=[('yes', 'Sim'), ('no', 'Não'), ('sometimes', 'Às Vezes')], max_length=20)),
                ('sociable_with_children', models.CharField(choices=[('yes', 'Sim'), ('no', 'Não'), ('sometimes', 'Às Vezes')], max_length=20)),
                ('sociable_with_strangers', models.CharField(choices=[('yes', 'Sim'), ('no', 'Não'), ('sometimes', 'Às Vezes')], max_length=20)),
                ('behavior', models.CharField(help_text='Ex: Medroso, Agitado, Calmo, etc.', max_length=100)),
                ('observations', models.TextField(blank=True, help_text='Observações ou cuidados especiais', null=True)),
                ('location', models.CharField(help_text='Endereço onde o pet está localizado', max_length=255)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('photo_1', models.ImageField(blank=True, null=True, upload_to='pet_adoption_photos/')),
                ('photo_2', models.ImageField(blank=True, null=True, upload_to='pet_adoption_photos/')),
                ('photo_3', models.ImageField(blank=True, null=True, upload_to='pet_adoption_photos/')),
                ('terms_accepted', models.BooleanField(default=False)),
                ('privacy_policy_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets_for_adoption', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
