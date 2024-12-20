# Generated by Django 4.2.8 on 2024-12-13 07:34

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_remove_product_age_class_remove_product_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='valid_from',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='valid_to',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_percentage',
            field=models.IntegerField(default=0, verbose_name='درصد تخفیف'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='end_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ پایان'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='start_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ شروع'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=50, unique=True, verbose_name='کد کوپن'),
        ),
    ]
