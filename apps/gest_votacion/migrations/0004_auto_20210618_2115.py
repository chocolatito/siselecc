# Generated by Django 3.1 on 2021-06-18 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gest_votacion', '0003_auto_20210617_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='urna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest_votacion.urna'),
        ),
    ]
