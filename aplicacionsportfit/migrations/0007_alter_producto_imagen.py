# Generated by Django 4.2.5 on 2024-06-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionsportfit', '0006_alter_producto_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]
