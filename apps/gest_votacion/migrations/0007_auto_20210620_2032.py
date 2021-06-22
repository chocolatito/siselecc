# Generated by Django 3.1 on 2021-06-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_votacion', '0006_voto_clave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='estado_voto',
            field=models.IntegerField(choices=[(0, 'EMITIDO'), (1, 'SUMADO')], default=0, verbose_name='Estado de voto'),
        ),
    ]
