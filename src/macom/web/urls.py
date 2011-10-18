
from django.conf.urls.defaults import patterns, url 
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from macom.diagrama.models import System, Module, Interface, Dependency
from macom.web.views import SystemDetailView, ModuleDetailView, \
    InterfaceDetailView, system_diagram, module_diagram, interface_diagram, systems_dependencies_diagram, \
    systems_no_thirdparty_dependencies_diagram
    
urlpatterns = patterns('',
     url(r'^$', lambda x: redirect('system_list')),
     url(r'^system/(?P<pk>\d+)/diagram', system_diagram, name='system_diagram'),
     url(r'^system/(?P<pk>\d+)', SystemDetailView.as_view(), name='system_detail'),
     url(r'^system[s]?/diagram/dependencies$', systems_dependencies_diagram, name='systems_dependencies_diagram'),
     url(r'^system[s]?/diagram/dependencies/no-thirdparty$', systems_no_thirdparty_dependencies_diagram, name='systems_no_thirdparty_dependencies_diagram'),
     url(r'^system[s/]?$', ListView.as_view(model=System), name='system_list'),
     url(r'^module/(?P<pk>\d+)/diagram', module_diagram, name='module_diagram'),
     url(r'^module/(?P<pk>\d+)', ModuleDetailView.as_view(), name='module_detail'),
     url(r'^module[s/]?$', ListView.as_view(model=Module), name='module_list'),
     url(r'^interface/(?P<pk>\d+)/diagram', interface_diagram, name='interface_diagram'),
     url(r'^interface/(?P<pk>\d+)', InterfaceDetailView.as_view(), name='interface_detail'),
     url(r'^interface[s/]?$', ListView.as_view(model=Interface), name='interface_list'),
     url(r'^dependency/(?P<pk>\d+)', DetailView.as_view(model=Dependency), name='dependency_detail'),
     url(r'^dependency[s/]?$' , ListView.as_view(model=Dependency), name='dependency_list'),
)
