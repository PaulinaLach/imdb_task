# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171202_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='startYear',
            field=models.SmallIntegerField(null=True),
        ),
    ]
