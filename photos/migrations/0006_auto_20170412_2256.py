# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 22:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20170412_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='subCategory',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
