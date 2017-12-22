#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^post-job/$', views.post_job, name='post_job'),
    url(r'^$', views.index),
]
