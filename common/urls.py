#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.index),
]
