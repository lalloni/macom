'''
Created on 09/03/2011

@author: sebas
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^png$', 'diagrama.views.png'),
    (r'^download/(?P<size>\d+)$', 'diagrama.views.download'),
    (r'^detail$', 'diagrama.views.detail'),
    url(r'^system-detail/(?P<id>\d+)$', 'diagrama.views.system_detail', name='system_detail'),
    url(r'^module-detail/(?P<id>\d+)$', 'diagrama.views.module_detail', name='module_detail'),
    url(r'^interface-detail/(?P<id>\d+)$', 'diagrama.views.interface_detail', name='interface_detail'),
    (r'^$', 'diagrama.views.detail'),
)