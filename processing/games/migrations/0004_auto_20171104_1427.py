# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_gamecomponent'),
    ]

    operations = [
        migrations.AddField(
            model_name='basegame',
            name='GMSlot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='basegame',
            name='observerSlot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='basegame',
            name='playerNumber',
            field=models.IntegerField(default=0),
        ),
    ]