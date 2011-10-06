'''
Created on 06/10/2011

@author: plalloni
'''
from django.conf.urls.defaults import patterns, url
from macom.app.views import app, script_template

urlpatterns = patterns('',
    url(r'^$', app, name="app"),
    url(r'^(?P<script_name>.*\.js)$', script_template, name='script_template'),
)
