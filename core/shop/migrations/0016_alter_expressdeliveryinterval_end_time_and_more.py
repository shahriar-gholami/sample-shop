# Generated by Django 4.2.15 on 2024-11-30 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_expressdeliveryinterval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expressdeliveryinterval',
            name='end_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='expressdeliveryinterval',
            name='start_time',
            field=models.IntegerField(),
        ),
    ]
