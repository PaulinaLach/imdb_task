# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171202_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='runtimeMinutes',
            field=models.DurationField(null=True),
        ),
    ]
