from django.conf.urls import url, include
# from django.contrib.auth import views
from . import views

urlpatterns = [
    url(r'^', views.StartPageView.as_view(), name='startPage'),
]