'''
Created on 09/03/2011

@author: sebas
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^maximize_all$', 'diagrama.views.maximize_all', name='maximize_all$'),
    url(r'^minimize/(?P<entity>.+)/(?P<id>\d+)$', 'diagrama.views.minimize', name='minimize'),
    url(r'^maximize/(?P<entity>.+)/(?P<id>\d+)$', 'diagrama.views.maximize', name='maximize'),
    
    (r'^png$', 'diagrama.views.png'),
    (r'^download/(?P<size>\d+)$', 'diagrama.views.download'),
    (r'^detail$', 'diagrama.views.detail'),
    (r'^$', 'diagrama.views.detail'),
)