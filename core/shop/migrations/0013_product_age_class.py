# Generated by Django 4.2.8 on 2024-11-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='age_class',
            field=models.IntegerField(default=1),
        ),
    ]
