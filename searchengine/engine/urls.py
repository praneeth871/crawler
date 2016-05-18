__author__ = 'praneeth.lakmala'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/search/$', views.search, name='search'),
]