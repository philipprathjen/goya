# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-08 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20160607_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_id', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='school',
            name='fb_id',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='jobs',
            field=models.ManyToManyField(to='profiles.Job'),
        ),
    ]
