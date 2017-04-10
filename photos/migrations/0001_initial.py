# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import photos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.CharField(default=photos.models.getTimeHex, max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, default='')),
                ('uploadDate', models.DateTimeField(auto_now_add=True)),
                ('source', models.ImageField(upload_to='source')),
                ('iso', models.CharField(blank=True, default='', max_length=128)),
                ('lens', models.CharField(blank=True, default='', max_length=128)),
                ('focal_length', models.CharField(blank=True, default='', max_length=128)),
                ('exposure_time', models.CharField(blank=True, default='', max_length=128)),
                ('takenDate', models.CharField(blank=True, default='', max_length=128)),
                ('aperture', models.CharField(blank=True, default='', max_length=128)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='photos.Category')),
            ],
        ),
    ]
