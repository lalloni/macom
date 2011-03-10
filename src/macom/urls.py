# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, handler404, handler500 #@UnusedImport
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    #(r'^polls/', include('polls.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),

)
