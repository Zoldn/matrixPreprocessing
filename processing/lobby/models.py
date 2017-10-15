# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Lobby(models.Model):

    lobbyName = models.CharField(max_length=255)
    password = models.CharField(max_length=20, blank=True)
    isPublic = models.IntegerField()
    totalSlots = models.IntegerField()
    occupiedSlots = models.IntegerField()



