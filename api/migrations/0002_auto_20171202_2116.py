# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='deathYear',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='endYear',
            field=models.SmallIntegerField(null=True),
        ),
    ]
