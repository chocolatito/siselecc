# Generated by Django 3.1 on 2021-11-07 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gest_votacion', '0008_auto_20211013_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voto',
            name='create_at',
        ),
    ]
