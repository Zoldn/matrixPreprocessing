from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.LobbyShortView.as_view(), name='showLobby'),
    url(r'^list/$', views.LobbyListView.as_view(), name='showLobbies'),
    url(r'^create/$', views.CreateLobbyView.as_view(), name='createLobby'),
    url(r'^(?P<pk>\d+)/update/$', views.LobbyUpdateView.as_view(), name='updateLobby'),
    url(r'^(?P<pk>\d+)/delete/$', views.LobbyDeleteView.as_view(), name='deleteLobby'),
    url(r'^(?P<pk>\d+)/join/$', views.JoinLobby.as_view(), name='joinLobby'),
    url(r'^(?P<pk>\d+)/join/password/$', views.PasswordInputJoinLobby.as_view(), name='passwordInput'),
    url(r'failed/noslots/$', views.JoinLobbyFailedNoSlots.as_view(), name='joinFailNoSlots'),
    url(r'^(?P<pk>\d+)/leave/$', views.LeaveLobbyView.as_view(), name='leaveLobby'),
    url(r'^(?P<pk>\d+)/kick/(?P<kicked>\d+)$', views.KickHimView.as_view(), name='kickFromLobby'),
    url(r'^join/$', views.JoinViaCodeView.as_view(), name='joinByCode'),
]