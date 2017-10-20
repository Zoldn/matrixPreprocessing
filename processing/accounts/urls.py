from django.conf.urls import url, include
from . import views
# from django.contrib.auth import views
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='showRegister'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='showProfile'),
    url(r'^login/$', views.LoginView.as_view(), name='Login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='Logout'),
    # url(r'^$', views.acc_login_or_register, name='accLoginOrRegister'),
    # url(r'^login/', views.acc_login, name='accLogin'),
    # url(r'^logout/', views.acc_logout, name='accLogout'),
    # url(r'^register/', views.acc_register, name='accRegister'),
    # url('^', include('django.contrib.auth.urls')),
]