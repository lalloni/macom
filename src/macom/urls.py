# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, handler404, handler500, url #@UnusedImport
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^diagrama/', include('diagrama.urls')),
    #(r'^polls/', include('polls.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^static-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}, name='static_media'),
)
