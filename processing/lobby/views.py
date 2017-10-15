# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import DetailView, ListView
from .models import Lobby
# Create your views here.


class LobbyShortView(DetailView):  # One-line view of Lobby for list

    model = Lobby
    template_name = 'lobby_template.html'


class LobbyListView(ListView):

    template_name = 'lobby_list.html'
    model = Lobby

    def dispatch(self, request, *args, **kwargs):
        self.sort_field = request.GET.get('sort_field')
        return super(LobbyListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Lobby.objects.all()
        if self.sort_field:
            queryset = queryset.order_by(self.sort_field)
        return queryset[:10]


def show_lobbies(request):
    lobbies = Lobby.objects.all()
    print lobbies[0]
    ret = render(request, 'lobby_list.html', {'lobbies': lobbies})
    return ret


def create_lobby(request):
    return HttpResponse('Lobby create')


def join_lobby(request):
    return HttpResponse('Join lobby')

