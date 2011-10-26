# -*- coding: UTF-8 -*-
from os import path
from django.conf.urls.defaults import patterns, url
from macom.app.views import app, script_template

urlpatterns = patterns('',
    url(r'^$', app, name="app"),
    url(r'^(?P<script_name>.*\.js)$', script_template, name='script_template'),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(path.dirname(__file__), 'images')})
)
