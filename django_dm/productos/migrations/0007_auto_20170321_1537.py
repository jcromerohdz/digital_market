# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_producto_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
