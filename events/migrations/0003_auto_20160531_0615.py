# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-31 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160530_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=250),
        ),
    ]