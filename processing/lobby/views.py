# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def show_lobbies(request):
    print request.user
    return HttpResponse(u'Test')
