'''
Created on 09/03/2011

@author: sebas
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
   (r'^$', 'diagrama.views.root'),
   (r'^filter/(?P<format>.+)/(?P<view>.+)/(?P<show>.*)/(?P<minimized>.*)/(?P<related>.*)$', 'diagrama.views.filter'),
   (r'^filter$', 'diagrama.views.filter'),
   (r'^show/(?P<format>.+)$', 'diagrama.views.show'),
   (r'^download/(?P<format>.+)/(?P<view>.+)/(?P<show>.*)/(?P<minimized>.*)/(?P<related>.*)$', 'diagrama.views.download'),
)
