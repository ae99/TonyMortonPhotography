# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0009_auto_20170413_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='original',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]