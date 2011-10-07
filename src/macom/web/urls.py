
from django.conf.urls.defaults import patterns, url 
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from macom.diagrama.models import System, Dependency, Interface, Module
    
def model_urls(args):
    (model, name) = args
    return [
            url(r'^%s[s/]?$' % name, ListView.as_view(model=model), name='%s_list' % name),
            url(r'^%s/(?P<pk>\d+)/' % name, DetailView.as_view(model=model), name='%s_detail' % name),
           ]

urlpatterns = patterns('', *
    [url(r'^$', lambda x: redirect('system_list'))] + 
    reduce(
           lambda x, y: x + y, 
           map(
               model_urls, 
               [
                (System, 'system'), 
                (Module, 'module'), 
                (Interface, 'interface'), 
                (Dependency, 'dependency'),
               ]
              )
          )
)
