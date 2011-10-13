# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}, name='media'),
    
    url(r'^diagrama/', include('macom.diagrama.urls')),
    
    url(r'^app/', include('macom.app.urls')),
    url(r'^api/', include('macom.api.urls')),
    url(r'^web/', include('macom.web.urls')),
    
)
