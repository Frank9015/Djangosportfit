# Generated by Django 4.2.5 on 2024-07-02 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aplicacionsportfit', '0014_usuario2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
                ('fecha_contacto', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_venta', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacionsportfit.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recibo_pdf', models.FileField(upload_to='recibos/')),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('venta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aplicacionsportfit.venta')),
            ],
        ),
        migrations.CreateModel(
            name='FichaPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('imc', models.FloatField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('imc', models.FloatField(blank=True, null=True)),
                ('comentarios', models.TextField()),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacionsportfit.fichapaciente')),
            ],
        ),
    ]
