# Generated by Django 4.2.8 on 2024-11-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_meta_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='shop.productcolor'),
        ),
    ]