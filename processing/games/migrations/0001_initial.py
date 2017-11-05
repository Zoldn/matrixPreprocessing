# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lobby', '0009_auto_20171020_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lobby.Lobby')),
            ],
        ),
    ]