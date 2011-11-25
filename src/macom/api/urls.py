# -*- coding: UTF-8 -*-
from piston.resource import Resource
from django.conf.urls.defaults import patterns, url, include
from macom.api.handlers import SystemHandler, ModuleHandler, InterfaceHandler, ModelHandler, DependencyHandler, \
    ReverseDependencyHandler
from piston.emitters import Emitter
from cStringIO import StringIO
import codecs
import csv

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode('utf-8') for s in row])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class CSVEmitter(Emitter):
    def render_record(self, element):
        record = []
        for field_name in element:
            field_value = element[field_name]
            if type(field_value) in [bool, int, long]:
                field_value = unicode(field_value)
            if 'encode' in dir(field_value):
                record.append(field_value)
        return record
    def render(self, request):
        data = self.construct()
        f = StringIO()
        try:
            w = UnicodeWriter(f)
            if type(data) in [list]:
                for element in data:
                    w.writerow(self.render_record(element))
            else:
                w.writerow(self.render_record(data))
            return f.getvalue()
        finally:
            f.close()

Emitter.register('csv', CSVEmitter, 'text/csv; charset=utf-8')

system_resource = Resource(SystemHandler)
module_resource = Resource(ModuleHandler)
interface_resource = Resource(InterfaceHandler)
dependency_resource = Resource(DependencyHandler)
reverse_dependency_resource = Resource(ReverseDependencyHandler)

reverse_dependencies = patterns('',
    url(r'reverse_dependenc(?:y|ies)/?$', reverse_dependency_resource)
)

dependencies = patterns('',
    url(r'^dependenc(?:y|ies)/?$', dependency_resource, name='api_dependency_list'),
    url(r'^dependency/(?P<dependency>\d+)/?$', dependency_resource, name='api_dependency'),
)

interfaces = patterns('',
    url(r'^interfaces?/?$', interface_resource, name='api_interface_list'),
    url(r'^interface/(?P<interface>\d+)/?$', interface_resource, name='api_interface'),
    url(r'^interface/(?P<interface>\d+)/', include(reverse_dependencies)),
)

modules = patterns('',
    url(r'^modules?/?$', module_resource, name='api_module_list'),
    url(r'^module/(?P<id>\d+)/?$', module_resource, name='api_module'),
    url(r'^module/(?P<module>\d+)/', include(interfaces)),
    url(r'^module/(?P<module>\d+)/', include(dependencies)),
    url(r'^module/(?P<module>\d+)/', include(reverse_dependencies)),
)

systems = patterns('',
    url(r'^systems?/?$', system_resource, name='api_system_list'),
    url(r'^system/(?P<id>\d+)/?$', system_resource, name='api_system'),
    url(r'^system/(?P<system>\d+)/', include(modules)),
    url(r'^system/(?P<system>\d+)/', include(interfaces)),
    url(r'^system/(?P<system>\d+)/', include(dependencies)),
    url(r'^system/(?P<system>\d+)/', include(reverse_dependencies)),
)

urlpatterns = patterns('',

    ('', include(systems)),
    ('', include(modules)),
    ('', include(interfaces)),
    ('', include(dependencies)),

    url(r'^model$', Resource(ModelHandler), name='api_model'),

)
