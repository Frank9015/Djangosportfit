# Generated by Django 4.2.5 on 2024-07-04 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0025_recibo_metodo_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='metodo_pago',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='metodo_pago',
        ),
    ]