# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.urls import reverse
# from lobby.models import Lobby
from django.contrib.postgres.fields import JSONField
from enum import IntEnum
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import models
import sys
from random import shuffle


class PlayerRoles(IntEnum):
    role_none = 0
    role_player = 1
    role_observer = 2
    role_ai = 3


class GameStatus(IntEnum):
    STATUS_NONE = 0
    STATUS_LOBBY = 1
    STATUS_GAME = 2
    STATUS_POSTGAME = 3


# Create your models here.

class Game(models.Model):
    # This is core model for the whole game structure. Game Modules, Lobbies and other stuff

    status = models.IntegerField(default=GameStatus.STATUS_LOBBY)

    def get_lobby(self):
        return get_object_or_404(Lobby, game=self.id)

    def get_module(self):
        return get_object_or_404(GameModule, game=self.id)

    def get_absolute_url(self):
        return reverse('game_redirector', args=str(self.id))

    def __str__(self):
        return self.get_lobby().lobbyName


class GameComponentModel(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True

    def get_game(self):
        return self.game


class Lobby(GameComponentModel):

    lobbyName = models.CharField(max_length=255)
    password = models.CharField(max_length=20, blank=True)
    isPublic = models.BooleanField(default=True)
    totalSlots = models.PositiveIntegerField(default=1)
    occupiedSlots = models.PositiveIntegerField(default=1)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    key = models.CharField(max_length=16, unique=True)

    def get_absolute_url(self):
        return reverse('showLobby', args=str(self.id))

    def __str__(self):
        return self.lobbyName


class GameModule(GameComponentModel):

    playerRoles = JSONField()
    playerNumber = models.IntegerField(default=0)
    observerSide = models.IntegerField(default=0)
    GMSide = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('curGameView', args=[str(self.id)])

    def __str__(self):
        return 'game {' + self.lobby.lobbyName + '}'

    def get_player_side(self, player_id):
        ret = -1
        for player in self.playerRoles[u'roles']:
            if player[u'id'] == player_id:
                ret = player[u'side']
        return ret

    def get_player_role(self, player_id):
        ret = PlayerRoles.role_none
        for player in self.playerRoles[u'roles']:
            if player[u'id'] == player_id:
                ret = player[u'role']
        return PlayerRoles(ret)

    def get_player_id(self, player_side):
        ret = -1
        for player in self.playerRoles[u'roles']:
            if player[u'side'] == player_side:
                ret = player[u'id']
        return ret

    def add_player(self, player_id, player_side, player_role):
        self.playerRoles[u'roles'].append(
            {
                u'id': player_id,
                u'role': player_role,
                u'side': player_side
            }
        )

    def get_visible_components(self, klass, player_side):
        filter_dict = {
            'visibility__values__' + str(player_side) + '__gt': 0,
            'game__id': self.id
        }
        return klass.objects.all().filter(**filter_dict)


class DbBaseModuleComponent(models.Model):

    class Meta:
        abstract = True

    module = models.ForeignKey(GameModule, on_delete=models.CASCADE, null=True, default=None)
    visibility = JSONField()
    owner = models.IntegerField(default=-1)
    setting = models.CharField(max_length=128)
    data = JSONField()
    gid = models.IntegerField()

    def init_visibility(self, player_number):
        self.visibility[u'values'] = [0] * player_number

    def change_visibility(self, player_side, value):
        self.visibility[u'values'][player_side] = value

    def get_visibility(self, player_side):
        return self.visibility[u'values'][player_side]


class DbModuleComponent(DbBaseModuleComponent):

    class_name = models.CharField(max_length=128)

    def load(self):
        klass = getattr(sys.modules[__name__], self.class_name)
        return klass(self)


class ModuleComponent:

    def __init__(self, db_item):
        self.db_item = db_item
        self.unpack(db_item.data)

    def pack(self):  # пакует данные объекта в словарь
        self.db_item.data = self.prepair_data()

    def save(self):
        self.pack()
        self.db_item.save()

    def unpack(self, data):  # OVERRIDE, распаковывает данные из JSONField словаря
        pass

    def prepare_data(self):  # OVERRIDE, возвращает словарь данных объекта для запаковки
        return {}

    def print_info(self, visibility_level):  # OVERRIDE, выводит инфу по объекту в виде словаря в зависимости от уровня
        # видимости
        return {}


class DbComponentDeck(DbBaseModuleComponent):

    refill_deck = models.IntegerField(null=True)
    discard_deck = models.IntegerField(null=True)
    limit = models.IntegerField(default=None, null=True)

    def load(self):
        return ModuleComponentDeck(self)


class ModuleComponentDeck:
    def __init__(self, db_item):
        self.db_item = db_item
        self.items = []
        self.refill_deck = None
        self.discard_deck = None
        self.limit = None
        self.name = u'Deck name missing'
        self.unpack(db_item.data)

    def unpack(self, data):
        self.items = data[u'items']
        self.refill_deck = data[u'refill_deck']
        self.discard_deck = data[u'discard_deck']
        self.limit = data[u'limit']
        self.name = data[u'name']

    def prepare_data(self):
        ret = {u'items': self.items,
               u'refill_deck': self.refill_deck,
               u'discard_deck': self.discard_deck,
               u'limit': self.limit}

    def print_info(self, visibility_level):
        ret = {}
        if visibility_level >= 1:
            ret = {u'id': self.gid,
                   u'name': self.name,
                   u'count': len(self.items)}

    def shuffle(self):
        shuffle(self.items)

