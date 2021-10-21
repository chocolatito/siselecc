# Generated by Django 3.1 on 2021-10-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_preparacion', '0016_eleccion_legajo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eleccion',
            name='legajo',
        ),
        migrations.AddField(
            model_name='eleccion',
            name='codigo',
            field=models.CharField(default=1, max_length=100, verbose_name='Codigo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eleccion',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]