# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import DetailView
from .models import Lobby
# Create your views here.


class LobbyShortView(DetailView):  # One-line view of Lobby for list

    model = Lobby
    template_name = 'lobby_template.html'


def show_lobbies(request):
    lobbies = Lobby.objects.all()
    print lobbies[0]
    ret = render(request, 'lobby_list.html', {'lobbies': lobbies})
    return ret
