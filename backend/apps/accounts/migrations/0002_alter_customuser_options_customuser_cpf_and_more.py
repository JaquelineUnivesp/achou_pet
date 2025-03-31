# Generated by Django 5.1.6 on 2025-03-05 14:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(blank=True, help_text='CPF no formato XXX.XXX.XXX-XX', max_length=14, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notification_phone',
            field=models.CharField(blank=True, help_text='Telefone para notificação', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notify_chat',
            field=models.BooleanField(default=True, help_text='Receber notificações de chat'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notify_other',
            field=models.BooleanField(default=True, help_text='Receber outras notificações'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notify_pet_found',
            field=models.BooleanField(default=True, help_text='Receber notificações de pet encontrado'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, help_text='Foto de perfil', null=True, upload_to='user_profiles/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]
