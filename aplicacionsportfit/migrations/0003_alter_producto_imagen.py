# Generated by Django 4.2.5 on 2024-06-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0002_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='img/productos'),
        ),
    ]