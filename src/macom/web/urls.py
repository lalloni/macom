from django.conf.urls.defaults import patterns, url 
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from macom.diagrama.models import System

urlpatterns = patterns('',
    url(r'^$', lambda x: redirect('system_list')),
    url(r'^system[s/]?$', ListView.as_view(model=System, context_object_name='system_list'), name='system_list'),
    url(r'^system/(?P<pk>\d+)/', DetailView.as_view(model=System, context_object_name='system'), name='system_detail'),
)
