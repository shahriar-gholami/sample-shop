# Generated by Django 4.2.8 on 2024-12-18 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_remove_filter_value_filtervalue_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtervalue',
            name='product',
            field=models.ManyToManyField(related_name='filter_values', to='shop.product'),
        ),
    ]
