# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.fields import PositiveIntegerField


class Lobby(models.Model):

    lobbyName = models.CharField(max_length=255)
    password = models.CharField(max_length=20, blank=True)
    isPublic = models.BooleanField(default=True)
    totalSlots = models.PositiveIntegerField(default=1)
    occupiedSlots = models.PositiveIntegerField(default=1)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')

    def get_absolute_url(self):
        return "/lobby/%i/" % self.id

    def __str__(self):
        return self.lobbyName

