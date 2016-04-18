# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^test$', views.test, name='test'),
    url(r'^auto/$', views.AutocompleteAdresse, name='AutocompleteAdresse'),
]
