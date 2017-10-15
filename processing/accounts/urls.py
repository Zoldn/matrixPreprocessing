from django.conf.urls import url, include
from . import views
from django.contrib.auth import views

urlpatterns = [
    # url(r'^$', views.acc_login_or_register, name='accLoginOrRegister'),
    # url(r'^login/', views.acc_login, name='accLogin'),
    # url(r'^logout/', views.acc_logout, name='accLogout'),
    # url(r'^register/', views.acc_register, name='accRegister'),
    # url('^', include('django.contrib.auth.urls')),
]