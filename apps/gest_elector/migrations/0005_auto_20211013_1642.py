# Generated by Django 3.1 on 2021-10-13 16:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_elector', '0004_auto_20210527_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elector',
            name='dni',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(9999999, message='Numero menor a un 10 millones'), django.core.validators.MaxValueValidator(99999999, message='Numero mayor o igual a un 100 millones')], verbose_name='DNI'),
        ),
    ]
