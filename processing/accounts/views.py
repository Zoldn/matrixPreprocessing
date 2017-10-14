# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.


def acc_login_or_register(request):
    return HttpResponse(u'Login or register')


def acc_login(request):
    return HttpResponse(u'Login')


def acc_logout(request):
    return HttpResponse(u'Logout')


def acc_register(request):
    return HttpResponse(u'Register')
