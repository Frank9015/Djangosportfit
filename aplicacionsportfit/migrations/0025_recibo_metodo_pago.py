# Generated by Django 4.2.5 on 2024-07-04 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0024_remove_recibo_metodo_pago_venta_metodo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='metodo_pago',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
