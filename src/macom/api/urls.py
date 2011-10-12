'''
Created on 06/10/2011

@author: plalloni
'''
from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from macom.api.handlers import SystemHandler, ModelHandler

system_resource = Resource(SystemHandler)

urlpatterns = patterns('',

    url(r'^system[s/]?$', system_resource, { 'emitter_format': 'json' }, name='api_system_list'),
    
    url(r'^system/(?P<id>\d+)$', system_resource, { 'emitter_format': 'json' }),

    url(r'^model$', Resource(ModelHandler), { 'emitter_format': 'json' }, name='api_model'),
    
)
