# Generated by Django 4.2.5 on 2024-07-04 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0026_remove_recibo_metodo_pago_remove_venta_metodo_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosenvio',
            name='ciudad',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='codigo_postal',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='direccion',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='estado',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='nombre_completo',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]
