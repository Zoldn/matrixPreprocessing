# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, FormView
from games.models import Lobby
from games.forms import LobbyListForm, EmptyForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import LoginForm
# Create your views here.


class ProfileView(ListView):

    template_name = 'profile.html'
    model = Lobby

    def dispatch(self, request, *args, **kwargs):
        self.form = LobbyListForm(request.GET)
        self.page = request.GET.get('page')
        self.profile_user = get_object_or_404(User, pk=kwargs['pk'])
        self.form.is_valid()
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Lobby.objects.all()
        # queryset = queryset.filter(isPublic=True)
        queryset = queryset.filter(members=self.profile_user)
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(lobbyName__icontains=self.form.cleaned_data['search'])
        if self.form.cleaned_data.get('sort_field'):
            queryset = queryset.order_by(self.form.cleaned_data['sort_field'])

        paginator = Paginator(queryset, 10)
        try:
            queryset = paginator.page(self.page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['profile_user'] = self.profile_user
        return context


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('showProfile',args=[user.id]))
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse_lazy('showProfile',args=[user.id]))
        else:
            return HttpResponseRedirect(reverse_lazy('Login'))
        # Return an 'invalid login' error message.


class LogoutView(FormView):
    template_name = 'logout.html'
    form_class = EmptyForm

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse_lazy('startPage'))