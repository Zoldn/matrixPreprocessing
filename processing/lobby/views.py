# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Lobby
from django.urls import reverse_lazy
from .forms import LobbyListForm, LobbyCreateForm, PasswordInputForm, EmptyForm, JoinViaCodeForm
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.crypto import get_random_string

# Create your views here.


class LobbyShortView(DetailView): # One-line view of Lobby for list

    model = Lobby
    template_name = 'lobby_detailed.html'

    def dispatch(self, request, *args, **kwargs):
        lobby = get_object_or_404(Lobby, pk=kwargs['pk'])
        if request.user in lobby.members.all():
            return super(LobbyShortView, self).dispatch(request, args, kwargs)
        else:
            if lobby.isPublic:
                return super(LobbyShortView, self).dispatch(request, args, kwargs)
            else:
                return HttpResponseForbidden()
                # return redirect(reverse_lazy('joinLobby', args=[lobby.id]))


class LobbyListView(ListView):

    template_name = 'lobby_list.html'
    model = Lobby

    def dispatch(self, request, *args, **kwargs):
        self.form = LobbyListForm(request.GET)
        self.page = request.GET.get('page')
        self.form.is_valid()
        return super(LobbyListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Lobby.objects.all()
        queryset = queryset.filter(isPublic=True)
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
        context = super(LobbyListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


class CreateLobbyView(LoginRequiredMixin, CreateView):

    model = Lobby
    fields = ['lobbyName', 'password', 'isPublic', 'totalSlots']
    template_name = 'lobby_create.html'

    def form_valid(self, form):
        form.instance.leader = self.request.user
        form.instance.key = get_random_string(length=16)
        if form.instance.totalSlots > 32:
            form.instance.totalSlots = 32
        ret = super(CreateLobbyView, self).form_valid(form)
        form.instance.members.add(self.request.user)
        return ret


class MyForbiddenException(Exception):
    pass


class LobbyUpdateView(LoginRequiredMixin, UpdateView):

    model = Lobby
    fields = ['lobbyName', 'password', 'isPublic', 'totalSlots']
    template_name = 'lobby_create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(LobbyUpdateView, self).dispatch(request, *args, **kwargs)
        except MyForbiddenException:
            return HttpResponseForbidden()

    def get_object(self, queryset=None):
        object_get = super(LobbyUpdateView, self).get_object(queryset)
        if object_get:
            if self.request.user.is_authenticated():
                if object_get.leader == self.request.user:
                    return object_get
        raise MyForbiddenException

    def form_valid(self, form):
        if form.instance.totalSlots > 32:
            form.instance.totalSlots = 32
        if form.instance.totalSlots < form.instance.members.count():
            form.instance.totalSlots = form.instance.members.count()
        return super(LobbyUpdateView, self).form_valid(form)


class LobbyDeleteView(LoginRequiredMixin, DeleteView):

    model = Lobby
    template_name = 'lobby_confirm_delete.html'
    success_url = '/lobby/list'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(LobbyDeleteView, self).dispatch(request, *args, **kwargs)
        except MyForbiddenException:
            return HttpResponseForbidden()

    def get_object(self, queryset=None):
        object_get = super(LobbyDeleteView, self).get_object(queryset)
        if object_get:
            if self.request.user.is_authenticated():
                if object_get.leader == self.request.user:
                    return object_get
        raise MyForbiddenException


class JoinLobby(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        lobby = get_object_or_404(Lobby, pk=kwargs['pk'])  # Lobby.objects.filter(pk=request.POST.get('pk'))
        if request.user in lobby.members.all():
            lobby.occupiedSlots = lobby.members.count()
            lobby.save()
            return HttpResponseRedirect(reverse_lazy('showLobby',args=[lobby.id]))
        else:
            if lobby.isPublic:
                if lobby.members.count() >= lobby.totalSlots:
                    return HttpResponseRedirect(reverse_lazy('joinFailNoSlots'))
                else:
                    if lobby.password:
                        return HttpResponseRedirect(reverse_lazy('passwordInput',args=[lobby.id]))
                    else:
                        lobby.members.add(request.user)
                        lobby.occupiedSlots = lobby.members.count()
                        lobby.save()
                        return HttpResponseRedirect(reverse_lazy('showLobby',args=[lobby.id]))
            else:
                return HttpResponseForbidden()


class PasswordInputJoinLobby(LoginRequiredMixin, FormView):

    template_name = 'lobby_password.html'
    form_class = PasswordInputForm

    def post(self, request, *args, **kwargs):
        self.lobby_id = kwargs['pk']
        self.user = request.user
        self.password = request.POST.get('password')
        return super(PasswordInputJoinLobby, self).post(request, args, kwargs)

    def form_valid(self, form):
        lobby = get_object_or_404(Lobby, pk=self.lobby_id)
        if self.password == lobby.password:
            if lobby.members.count() >= lobby.totalSlots:
                return HttpResponseRedirect(reverse_lazy('joinFailNoSlots'))
            else:
                lobby.members.add(self.user)
                lobby.occupiedSlots = lobby.members.count()
                lobby.save()
                return HttpResponseRedirect(reverse_lazy('showLobby', args=[lobby.id]))
        else:
            return HttpResponseRedirect(reverse_lazy('passwordInput', args=[lobby.id]))


class JoinLobbyFailedNoSlots(TemplateView):

    template_name = 'lobby_join_no_free_slots.html'


class LeaveLobbyView(LoginRequiredMixin, FormView):

    template_name = 'lobby_leave.html'
    form_class = EmptyForm

    def post(self, request, *args, **kwargs):
        self.lobby_id = kwargs['pk']
        self.user = request.user
        return super(LeaveLobbyView, self).post(request, args, kwargs)

    def form_valid(self, form):
        lobby = get_object_or_404(Lobby, pk=self.lobby_id)
        if self.user in lobby.members.all():
            lobby.members.remove(self.user)
            lobby.occupiedSlots = lobby.members.count()
            lobby.save()
            return HttpResponseRedirect(reverse_lazy('showLobbies'))
        else:
            return HttpResponse('OBJECTION! You are not in the lobby to leave it')


class KickHimView(LoginRequiredMixin, FormView):

    template_name = 'lobby_kick.html'
    form_class = EmptyForm

    def post(self, request, *args, **kwargs):
        self.lobby_id = kwargs['pk']
        self.kicked_id = kwargs['kicked']
        return super(KickHimView, self).post(request, args, kwargs)

    def form_valid(self, form):
        lobby = get_object_or_404(Lobby, pk=self.lobby_id)
        kicked = User.objects.get(id=self.kicked_id)
        if kicked and (kicked in lobby.members.all()):
            lobby.members.remove(kicked)
            lobby.occupiedSlots = lobby.members.count()
            lobby.save()
            return HttpResponseRedirect(reverse_lazy('showLobby', args=[lobby.id]))
        else:
            return HttpResponse('OBJECTION! He isnt in the lobby. You cant kick')


class JoinViaCodeView(LoginRequiredMixin, FormView):

    template_name = 'lobby_join_via_code.html'
    form_class = JoinViaCodeForm

    def post(self, request, *args, **kwargs):
        self.code = request.POST.get('code')
        return super(JoinViaCodeView, self).post(request, args, kwargs)

    def form_valid(self, form):
        # lobby = get_object_or_404(Lobby, key=self.code)
        lobby = Lobby.objects.all().filter(key=self.code)
        if lobby:
            if self.request.user in lobby.members.all():
                lobby.occupiedSlots = lobby.members.count()
                lobby.save()
                return HttpResponseRedirect(reverse_lazy('showLobby',args=[lobby.id]))
            else:
                if lobby.members.count() >= lobby.totalSlots:
                    return HttpResponseRedirect(reverse_lazy('joinFailNoSlots'))
                else:
                    lobby.members.add(self.request.user)
                    lobby.occupiedSlots = lobby.members.count()
                    lobby.save()
                    return HttpResponseRedirect(reverse_lazy('showLobby',args=[lobby.id]))
        else:
            return HttpResponseRedirect(reverse_lazy('joinByCode'))