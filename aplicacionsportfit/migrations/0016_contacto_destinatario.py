# Generated by Django 4.2.5 on 2024-07-02 15:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0015_contacto_venta_recibo_fichapaciente_evolucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='destinatario',
            field=models.CharField(choices=[('nutricionista', 'Nutricionista'), ('preparador_fisico', 'Preparador Físico')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]