# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-27 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='color',
            field=models.CharField(default='green', max_length=6),
        ),
    ]
