# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 14:34
from __future__ import unicode_literals

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import productos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MisProductos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Mis Productos',
                'verbose_name_plural': 'Mis Productos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/chris/Documents/Proyectos/git_dm/digital_market/django_dm/protected'), upload_to=productos.models.download_media_location)),
                ('nombre', models.CharField(max_length=40)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('descripcion', models.TextField(null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=9999)),
                ('precio_oferta', models.DecimalField(blank=True, decimal_places=2, max_digits=9999, null=True)),
                ('tipo', models.CharField(blank=True, default='foto', max_length=40, null=True)),
                ('administradores', models.ManyToManyField(blank=True, related_name='administradores_producto', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='misproductos',
            name='productos',
            field=models.ManyToManyField(blank=True, to='productos.Producto'),
        ),
        migrations.AddField(
            model_name='misproductos',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]