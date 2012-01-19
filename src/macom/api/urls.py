# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from macom.api.handlers import SystemHandler, ModuleHandler, InterfaceHandler, DependencyHandler, \
    ReverseDependencyHandler, TagHandler, ArchitecturalPatternHandler, ArchitecturalPatternCaseHandler
from macom.api.helpers import CSVEmitter
from piston.emitters import Emitter
from piston.resource import Resource

Emitter.register('csv', CSVEmitter, 'text/csv; charset=utf-8')

system_resource = Resource(SystemHandler)
module_resource = Resource(ModuleHandler)
interface_resource = Resource(InterfaceHandler)
dependency_resource = Resource(DependencyHandler)
reverse_dependency_resource = Resource(ReverseDependencyHandler)
architecturalpattern_resource = Resource(ArchitecturalPatternHandler)
architecturalpatterncase_resource = Resource(ArchitecturalPatternCaseHandler)
tag_resource = Resource(TagHandler)

reverse_dependencies = patterns('',
    url(r'reverse_dependenc(?:y|ies)/?$', reverse_dependency_resource)
)

dependencies = patterns('',
    url(r'^dependenc(?:y|ies)/?$', dependency_resource, name='api_dependency_list'),
    url(r'^dependency/(?P<dependency>\d+)/?$', dependency_resource, name='api_dependency'),
)

interfaces = patterns('',
    url(r'^interfaces?/?$', interface_resource, name='api_interface_list'),
    url(r'^(?P<model>interface)s/tags?/?$', tag_resource),
    url(r'^interface/(?P<interface>\d+)/?$', interface_resource, name='api_interface'),
    url(r'^interface/(?P<interface>\d+)/', include(reverse_dependencies)),
)

modules = patterns('',
    url(r'^modules?/?$', module_resource, name='api_module_list'),
    url(r'^(?P<model>module)s/tags?/?$', tag_resource),
    url(r'^module/(?P<id>\d+)/?$', module_resource, name='api_module'),
    url(r'^module/(?P<module>\d+)/', include(interfaces)),
    url(r'^module/(?P<module>\d+)/', include(dependencies)),
    url(r'^module/(?P<module>\d+)/', include(reverse_dependencies)),
)

systems = patterns('',
    url(r'^systems?/?$', system_resource, name='api_system_list'),
    url(r'^(?P<model>system)s/tags?/?$', tag_resource),
    url(r'^system/(?P<id>\d+)/?$', system_resource, name='api_system'),
    url(r'^system/(?P<system>\d+)/', include(modules)),
    url(r'^system/(?P<system>\d+)/', include(interfaces)),
    url(r'^system/(?P<system>\d+)/', include(dependencies)),
    url(r'^system/(?P<system>\d+)/', include(reverse_dependencies)),
)

architecturalpatterns = patterns('',
    url(r'^architecturalpatterns?/?$', architecturalpattern_resource, name='api_architecturalpattern_list'),
    url(r'^architecturalpattern/(?P<pattern>\d+)/?$', architecturalpattern_resource, name='api_architecturalpattern')
)

architecturalpatterncases = patterns('',
    url(r'^architecturalpatterncases?/?$', architecturalpatterncase_resource, name='api_architecturalpatterncase_list'),
    url(r'^architecturalpatterncase/(?P<id>\d+)/?$', architecturalpatterncase_resource, name='api_architecturalpatterncase')
)

tags = patterns('',
    url(r'^tags?/?$', tag_resource, name='api_tag_list'),
    url(r'^tag/(?P<slug>\w+)$', tag_resource, name='api_tag')
)

urlpatterns = patterns('',

    ('', include(systems)),
    ('', include(modules)),
    ('', include(interfaces)),
    ('', include(dependencies)),
    ('', include(architecturalpatterns)),
    ('', include(architecturalpatterncases)),
    ('', include(tags)),

)
