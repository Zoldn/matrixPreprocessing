from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/', views.LobbyShortView.as_view(), name='showLobby'),
    url(r'^list/$', views.show_lobbies, name='showLobbies'),
]