# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='original',
            field=models.ImageField(default=None, upload_to='original'),
        ),
    ]
