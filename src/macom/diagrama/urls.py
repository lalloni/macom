'''
Created on 09/03/2011

@author: sebas
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^maximize_all$', 'diagrama.views.maximize_all', name='maximize_all'),
    url(r'^minimize_all$', 'diagrama.views.minimize_all', name='minimize_all'),
    
    url(r'^open_all$', 'diagrama.views.open_all', name='open_all'),
    url(r'^close_all$', 'diagrama.views.close_all', name='close_all'),
    url(r'^show_related_systems$', 'diagrama.views.show_related_systems', name='show_related_systems'),
    url(r'^hide_related_systems$', 'diagrama.views.hide_related_systems', name='hide_related_systems'),
    
    url(r'^minimize/(?P<id>\d+)$', 'diagrama.views.minimize', name='minimize'),
    url(r'^maximize/(?P<id>\d+)$', 'diagrama.views.maximize', name='maximize'),
    url(r'^close/(?P<id>\d+)$', 'diagrama.views.close', name='close'),
    url(r'^open/(?P<id>\d+)$', 'diagrama.views.open', name='open'),
    
    (r'^show/(?P<format>.+)$', 'diagrama.views.show'),
    (r'^download/(?P<size>\d+)/(?P<format>.+$)', 'diagrama.views.download'),
    (r'^detail$', 'diagrama.views.detail'),
    (r'^$', 'diagrama.views.detail'),
)
