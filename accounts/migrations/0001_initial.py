# Generated by Django 5.2.4 on 2025-07-12 02:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disciplinas', '0004_alter_cronogramadisciplina_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='disciplinas.curso', verbose_name='Curso')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Perfil de Usuário',
                'verbose_name_plural': 'Perfis de Usuários',
            },
        ),
    ]
