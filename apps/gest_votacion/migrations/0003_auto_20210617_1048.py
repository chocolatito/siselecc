# Generated by Django 3.1 on 2021-06-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_votacion', '0002_voto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urna',
            name='estado_urna',
            field=models.IntegerField(choices=[(0, 'CREADA'), (1, 'LIBRE'), (2, 'ESPERANDO ELECTOR'), (3, 'EN OPERACIÓN'), (4, 'EN CONFIRMACIÓN'), (5, 'OPERACION COMPLETADA'), (6, 'ELECTOR RETIRADO'), (7, 'CERRADA')], default=0, verbose_name='Estado de urna'),
        ),
    ]
