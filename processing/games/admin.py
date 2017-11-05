# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Game, Lobby, GameModule
# Register your models here.

admin.site.register(Game)
admin.site.register(Lobby)
admin.site.register(GameModule)
