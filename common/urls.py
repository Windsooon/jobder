#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^$', views.index),
]
