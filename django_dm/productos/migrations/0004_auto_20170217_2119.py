# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_auto_20170217_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='slug',
            field=models.SlugField(default='slug-field'),
        ),
    ]