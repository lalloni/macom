'''
Created on 06/10/2011

@author: plalloni
'''
from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from macom.api.handlers import SystemHandler, ModuleHandler, InterfaceHandler, ModelHandler, DependencyHandler

system_resource = Resource(SystemHandler)
module_resource = Resource(ModuleHandler)
interface_resource = Resource(InterfaceHandler)
dependency_resource = Resource(DependencyHandler)

urlpatterns = patterns('',

    url(r'^system[s/]?$', system_resource, { 'emitter_format': 'json' }, name='api_system_list'),
    url(r'^system/(?P<id>\d+)$', system_resource, { 'emitter_format': 'json' }, name='api_system'),

    url(r'^module[s/]?$', module_resource, { 'emitter_format': 'json' }, name='api_module_list'),
    url(r'^module/(?P<id>\d+)$', module_resource, { 'emitter_format': 'json' }, name='api_module'),

    url(r'^interface[s/]?$', interface_resource, { 'emitter_format': 'json' }, name='api_interface_list'),
    url(r'^interface/(?P<id>\d+)$', interface_resource, { 'emitter_format': 'json' }, name='api_interface'),

    url(r'^dependency[s/]?$', dependency_resource, { 'emitter_format': 'json' }, name='api_dependency_list'),
    url(r'^dependency/(?P<id>\d+)$', dependency_resource, { 'emitter_format': 'json' }, name='api_dependency'),

    url(r'^model$', Resource(ModelHandler), { 'emitter_format': 'json' }, name='api_model'),

)
