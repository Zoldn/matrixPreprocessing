# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20171104_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basegame',
            old_name='GMSlot',
            new_name='GMSide',
        ),
        migrations.RenameField(
            model_name='basegame',
            old_name='observerSlot',
            new_name='observerSide',
        ),
    ]