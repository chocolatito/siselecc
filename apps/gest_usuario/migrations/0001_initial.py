# Generated by Django 3.1 on 2021-05-21 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gest_elector', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('tipo', models.IntegerField(choices=[(0, 'STAFF'), (1, 'ELECTOR')], default=1, verbose_name='Tipo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
                'ordering': ['tipo'],
            },
        ),
        migrations.CreateModel(
            name='CuentaElector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('confirmacion', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de confirmación')),
                ('estado_confirmacion', models.BooleanField(default=False, verbose_name='Estado de confirmación')),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gest_usuario.cuenta', verbose_name='Cuenta')),
                ('elector', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gest_elector.elector', verbose_name='Elector')),
            ],
            options={
                'verbose_name': 'CuentaElector',
                'verbose_name_plural': 'CuentasElector',
                'ordering': ['creacion'],
            },
        ),
    ]
