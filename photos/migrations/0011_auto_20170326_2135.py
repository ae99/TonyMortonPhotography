# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0010_photo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
