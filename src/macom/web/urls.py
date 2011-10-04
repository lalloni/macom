from django.conf.urls.defaults import patterns, url

from diagrama.models import *
from django.views.generic import ListView

urlpatterns = patterns('',

    (r'^sys/$', ListView.as_view(
        model=System,
    )),

    (r'^$', 'web.views.index'),

    (r'^system.$', 'web.views.system'),
    (r'^system/(?P<id>.+)$', 'web.views.systemdetail'),

    (r'^system.module.$', 'web.views.module'),
    (r'^system.module/(?P<id>.+)$', 'web.views.moduledetail'),

    #(r'^dependency.$', 'web.views.dependency'),
    #(r'^dependency/(?P<id>.+)$', 'web.views.dependencydetail'),
)

