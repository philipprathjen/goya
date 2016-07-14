# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-12 14:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 12, 14, 55, 19, 346215, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 12, 14, 55, 33, 449070, tzinfo=utc)),
            preserve_default=False,
        ),
    ]