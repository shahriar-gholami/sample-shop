# Generated by Django 4.2.8 on 2024-11-19 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]