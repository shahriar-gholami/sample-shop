# Generated by Django 4.2.8 on 2024-12-18 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter',
            name='value',
        ),
        migrations.AddField(
            model_name='filtervalue',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.filter'),
        ),
    ]
