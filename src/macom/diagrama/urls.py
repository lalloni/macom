'''
Created on 09/03/2011

@author: sebas
'''
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^png$', 'diagrama.views.png'),
    (r'^detalle$', 'diagrama.views.detalle'),
    (r'^$', 'diagrama.views.detalle'),
)