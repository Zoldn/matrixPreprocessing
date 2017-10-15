from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/', views.LobbyShortView.as_view(), name='showLobby'),
    url(r'^list/$', views.LobbyListView.as_view(), name='showLobbies'),
    url(r'^create/$', views.create_lobby, name='createLobby'),
    url(r'^join/(?P<lobby_id>\d+)/', views.join_lobby, name='joinLobby'),
]