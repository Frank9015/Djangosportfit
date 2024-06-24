# Generated by Django 4.2.5 on 2024-06-24 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aplicacionsportfit', '0009_usuario_delete_usu_registrado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('cliente', 'Cliente'), ('superadmin', 'Superadmin'), ('preparador_fisico', 'Preparador Físico'), ('nutricionista', 'Nutricionista')], default='cliente', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
