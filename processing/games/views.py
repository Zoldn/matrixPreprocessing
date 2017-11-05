# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import DetailView
from . import models
# Create your views here.


class curGameView(DetailView):

    model = models.BaseGame
    template_name = 'game_detailed.html'
