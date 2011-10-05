# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^static-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}, name='static_media'),
    
    (r'^diagrama/', include('macom.diagrama.urls')),
    
    (r'^', include('macom.web.urls')), # todo lo demás es la "web"
    
)
