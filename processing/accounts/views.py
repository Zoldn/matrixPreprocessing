# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

# Create your views here.


def show_profile(request):
    userName = request.user
    return render(request, 'profile.html', {'username': userName})
    # return HttpResponse(u'There will be your profile')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../profile/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})