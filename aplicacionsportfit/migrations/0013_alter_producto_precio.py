# Generated by Django 4.2.5 on 2024-06-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0012_rename_carrito_cartitem_cart_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.FloatField(),
        ),
    ]
