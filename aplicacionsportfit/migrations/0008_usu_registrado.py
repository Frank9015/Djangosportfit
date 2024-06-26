# Generated by Django 5.0.6 on 2024-06-17 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0007_alter_producto_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usu_registrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombres', models.CharField(max_length=100)),
                ('edad', models.PositiveIntegerField()),
                ('direccion', models.CharField(max_length=200)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('fecha_contrato', models.DateField()),
                ('fecha_termino', models.DateField()),
            ],
            options={
                'ordering': ['nombres'],
            },
        ),
    ]
