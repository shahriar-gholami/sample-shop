# Generated by Django 4.2.8 on 2024-12-12 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_brand_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='store',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='store',
        ),
        migrations.RemoveField(
            model_name='blogcategory',
            name='store',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='store',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='store',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='store',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='store',
        ),
        migrations.RemoveField(
            model_name='category',
            name='store',
        ),
        migrations.RemoveField(
            model_name='categoryimage',
            name='store',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='store',
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='store',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='store',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='store',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='store',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='store',
        ),
        migrations.RemoveField(
            model_name='featuredcategories',
            name='store',
        ),
        migrations.RemoveField(
            model_name='filter',
            name='store',
        ),
        migrations.RemoveField(
            model_name='filtervalue',
            name='store',
        ),
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='store',
        ),
        migrations.RemoveField(
            model_name='postthumbnail',
            name='store',
        ),
        migrations.RemoveField(
            model_name='product',
            name='store',
        ),
        migrations.RemoveField(
            model_name='productcolor',
            name='store',
        ),
        migrations.RemoveField(
            model_name='recommender',
            name='store',
        ),
        migrations.RemoveField(
            model_name='services',
            name='store',
        ),
        migrations.RemoveField(
            model_name='slide',
            name='store',
        ),
        migrations.RemoveField(
            model_name='storelogoimage',
            name='store',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='store',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='store',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='store',
        ),
        migrations.RemoveField(
            model_name='uploadedimages',
            name='store',
        ),
        migrations.RemoveField(
            model_name='withdrawrecord',
            name='store',
        ),
        migrations.AlterField(
            model_name='variety',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
