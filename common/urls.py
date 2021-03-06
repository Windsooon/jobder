#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.urls import re_path
from common import views

urlpatterns = [
    url(r'^post-job/$', views.post_job, name='post_job'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^pay/$', views.pay, name='pay'),
    url(r'^charge_su/$', views.charge_su, name='charge_su'),
    url(r'^repo-search/$', views.repo_search, name='repo_search'),
    url(r'^developers/$', views.contributors, name='contributors'),
    url(r'^posted-jobs/$', views.posted_jobs, name='posted_jobs'),
    url(r'^match/$', views.match, name='match'),
    url(r'^explain/$', views.explain, name='explain'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    re_path(
        r'^card_callback/(?P<post_id>[0-9]+)/$',
        views.card_callback, name='card_callback'),
    re_path(
        r'^job/(?P<id>[0-9]+)/$',
        views.job, name='job'),
    re_path(
        r'^(?P<name>([a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*){1,38})/$',
        views.card, name='card'),
    url(r'^$', views.index, name='front_page'),
]
