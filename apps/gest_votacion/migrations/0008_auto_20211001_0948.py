# Generated by Django 3.1 on 2021-10-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_votacion', '0007_auto_20210620_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='vector_cifrado',
            field=models.JSONField(verbose_name='Vector cifrado'),
        ),
    ]
