# Generated by Django 4.2.5 on 2024-07-04 17:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0023_alter_recibo_metodo_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='metodo_pago',
        ),
        migrations.AddField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
