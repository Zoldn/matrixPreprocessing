# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0005_auto_20171017_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='occupiedSlots',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='totalSlots',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
