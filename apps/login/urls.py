from django.conf.urls import url, include
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout)
]
