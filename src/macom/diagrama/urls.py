# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns, url #@UnusedImport

urlpatterns = patterns('',
   (r'^$', 'diagrama.views.root'),
   (r'^filter/(?P<format>.+)/(?P<view>.+)/(?P<show>.*)/(?P<minimized>.*)/(?P<related>.*)$', 'diagrama.views.filter'),
   (r'^filter$', 'diagrama.views.filter'),
   (r'^show/(?P<format>.+)$', 'diagrama.views.show'),
   (r'^download/(?P<format>.+)/(?P<view>.+)/(?P<show>.*)/(?P<minimized>.*)/(?P<related>.*)$', 'diagrama.views.download'),
)
