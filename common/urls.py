#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.urls import path, re_path
from common import views

urlpatterns = [
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^post-job/$', views.post_job, name='post_job'),
    url(r'^match/$', views.match, name='match'),
    url(r'^$', views.index, name='front_page'),
    re_path(
        r'^job/(?P<id>[0-9]+)/$',
        views.job, name='job'),
    re_path(
        r'^(?P<name>([a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*){1,38})/$',
        views.profile, name='profile'),
]
