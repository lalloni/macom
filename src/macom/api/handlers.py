# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from macom.api.helpers import callee_name
from macom.diagrama.models import System, Module, Interface, Dependency, ArchitecturalPattern, ArchitecturalPatternCase
from piston.handler import BaseHandler
from taggit.models import Tag, TaggedItem

def model_field(name, *args):
    return (name, ('kind', 'name') + args)

def collection_fields(name):
    return (name + '_uri', model_field(name))

def query_fields(name):
    return (name, name + '_uri')

class Defaults(BaseHandler):
    allowed_methods = ('GET',) # sólo lectura
    @classmethod
    def _kind(cls):
        return cls.model._meta.object_name.lower()
    @classmethod
    def kind(cls, m):
        return cls._kind()
    @classmethod
    def full_name(cls, m):
        return unicode(m)
    @classmethod
    def direction(cls, m):
        return m.direction()
    @classmethod
    def diagram_uri(cls, m):
        return reverse('web:%s_diagram' % cls._kind(), args=[m.pk])
    @classmethod
    def resource_uri(cls):
        return ('api_%s' % cls._kind(), ['pk'])
    @classmethod
    def kind_of(cls, m):
        return m.__class__._meta.object_name.lower()
    @classmethod
    def resource_uri_of(cls, m):
        return reverse('api_%s' % cls.kind_of(m), args=[m.pk])
    @classmethod
    def short_of(cls, m):
        return dict(kind=cls.kind_of(m), name=cls.full_name(m), resource_uri=cls.resource_uri_of(m))
    @classmethod
    def collection_uri(cls, m, name):
        return cls.resource_uri_of(m) + '/' + name[:-4]
    @classmethod
    def modules_uri(cls, m):
        return cls.collection_uri(m, callee_name())
    @classmethod
    def interfaces_uri(cls, m):
        return cls.collection_uri(m, callee_name())
    @classmethod
    def dependencies_uri(cls, m):
        return cls.collection_uri(m, callee_name())
    @classmethod
    def reverse_dependencies_uri(cls, m):
        return cls.collection_uri(m, callee_name())
    @classmethod
    def edit_url(cls, m):
        return reverse('admin:%s_%s_change' % (m._meta.app_label, m._meta.module_name), args=[m.pk])
    @classmethod
    def history_url(cls, m):
        return reverse('admin:%s_%s_history' % (m._meta.app_label, m._meta.module_name), args=[m.pk])
    @classmethod
    def tags(cls, m):
        return map(lambda tag: tag.name, m.tags.all())

class SystemHandler(Defaults):
    model = System
    fields = ('kind', 'name', 'full_name', 'external', 'description',
              'functional_referents', 'implementation_referents', 'documentation', 'diagram_uri',
              ('tags', ()),
              'edit_url', 'history_url') \
             + collection_fields('modules') \
             + collection_fields('interfaces') \
             + query_fields('dependencies') \
             + query_fields('reverse_dependencies')
    @classmethod
    def dependencies(cls, system):
        return map(cls.short_of, Dependency.objects.filter(module__system=system).exclude(interface__module__system=system))
    @classmethod
    def reverse_dependencies(cls, system):
        return map(cls.short_of, Dependency.objects.filter(interface__module__system=system).exclude(module__system=system))

class ModuleHandler(Defaults):
    model = Module
    fields = ('kind', 'name', 'full_name', 'external', 'goal',
              'functional_referents', 'implementation_referents', 'documentation', 'diagram_uri',
              ('tags', ()), model_field('system', 'full_name'),
              'edit_url', 'history_url') \
             + collection_fields('interfaces') \
             + query_fields('dependencies') \
             + query_fields('reverse_dependencies')
    @classmethod
    def dependencies(cls, module):
        return map(cls.short_of, module.dependency_objects())
    @classmethod
    def reverse_dependencies(cls, module):
        return map(cls.short_of, Dependency.objects.filter(interface__module=module).exclude(module=module))

class InterfaceHandler(Defaults):
    model = Interface
    fields = ('kind', 'name', 'full_name', 'external', 'goal',
              'published', 'technology', 'direction', 'loadestimate',
              'functional_referents', 'implementation_referents', 'documentation', 'diagram_uri',
              ('tags', ()), model_field('module', model_field('system')),
              'edit_url', 'history_url') \
             + query_fields('reverse_dependencies')
    @classmethod
    def read(cls, req, interface=None, system=None, module=None):
        if interface:
            return Interface.objects.get(id=interface)
        if module:
            return Interface.objects.filter(module=module)
        if system:
            return Interface.objects.filter(module__system=system)
        else:
            return Interface.objects.all()
    @classmethod
    def reverse_dependencies(cls, interface):
        return map(cls.short_of, Dependency.objects.filter(interface=interface))

class DependencyHandler(Defaults):
    model = Dependency
    fields = ('kind', 'full_name', 'goal',
              'technology', 'direction', 'loadestimate',
              'functional_referents', 'implementation_referents', 'documentation', 'diagram_uri',
              model_field('module', model_field('system')), model_field('interface', model_field('module', model_field('system'))),
              'edit_url', 'history_url')
    @classmethod
    def read(cls, req, dependency=None, system=None, module=None, interface=None):
        if dependency:
            return Dependency.objects.get(id=dependency)
        if interface:
            return Dependency.objects.filter(interface=interface)
        if module:
            return Dependency.objects.filter(module=module)
        if system:
            return Dependency.objects.filter(module__system=system).exclude(interface__module__system=system)
        else:
            return Dependency.objects.all()

class ReverseDependencyHandler(DependencyHandler):
    @classmethod
    def read(cls, req, system=None, module=None, interface=None):
        if interface:
            return Dependency.objects.filter(interface=interface)
        if module:
            return Dependency.objects.filter(interface__module=module).exclude(module=module)
        if system:
            return Dependency.objects.filter(interface__module__system=system).exclude(module__system=system)

class ArchitecturalPatternHandler(Defaults):
    model = ArchitecturalPattern
    fields = ('kind', 'name', 'description', ('tags', ())) + collection_fields('cases')
    @classmethod
    def read(cls, request, pattern=None):
        if pattern:
            return ArchitecturalPattern.objects.get(id=pattern)
        else:
            return ArchitecturalPattern.objects.all()

class ArchitecturalPatternCaseHandler(Defaults):
    model = ArchitecturalPatternCase
    fields = ('annotation', model_field('architecturalpattern'))

class TagHandler(Defaults):
    model = Tag
    fields = ('name',)
    @classmethod
    def resource_uri(cls):
        return ('api_tag', ['slug'])
    @classmethod
    def read(cls, req, slug=None, model=None):
        if model:
            models = [System, Module, Interface, ArchitecturalPattern]
            lookup = dict(zip(map(lambda model: model._meta.object_name.lower(), models), models))
            return TaggedItem.tags_for(lookup[model])
        if slug:
            return map(lambda i: i.content_object, TaggedItem.objects.select_related().filter(tag=Tag.objects.get(slug=slug)))
        else:
            return map(lambda i: dict(name=i['name'], count=i['count'], resource_uri=reverse('api_tag', args=[i['slug']])), Tag.objects.values('name', 'slug').annotate(count=Count('taggit_taggeditem_items')).order_by('-count'))

class ModelHandler(BaseHandler):
    def read(self, request):
        res = []
        for syst in System.objects.values('id', 'name', 'external'):
            syst['kind'] = "system"
            syst['resource_uri'] = reverse('api_system', args=[syst['id']])
            syst['full_name'] = syst['name']
            syst_id = syst['id']
            syst['id'] = "%s%s" % (syst['kind'], syst_id)
            res.append(syst)
            modus = []
            for modu in Module.objects.filter(system__id=syst_id).values('id', 'name', 'external'):
                modu['kind'] = "module"
                modu['resource_uri'] = reverse('api_module', args=[modu['id']])
                modu['full_name'] = "%s:%s" % (modu['name'], syst['name'])
                modu_id = modu['id']
                modu['id'] = "%s%s" % (modu['kind'], modu_id)
                modus.append(modu)
                intes = []
                for inte in Interface.objects.filter(module__id=modu_id).values('id', 'name'):
                    inte['kind'] = "interface"
                    inte['full_name'] = "%s:%s" % (modu['full_name'], inte['name'])
                    inte['resource_uri'] = reverse('api_interface', args=[inte['id']])
                    inte['id'] = "%s%s" % (inte['kind'], inte['id'])
                    intes.append(inte)
                modu['children'] = intes
            syst['children'] = modus
        return dict(kind='root',
                    name='Sistemas',
                    full_name='Sistemas',
                    resource_uri='root',
                    isOpen='true',
                    tagcloud_uri=reverse('api_tag_list'),
                    diagrams=[dict(name='Dependencias entre sistemas', diagram_uri=reverse('web:systems_dependencies_diagram')),
                              dict(name='Dependencias entre sistemas (excluyendo externos)', diagram_uri=reverse('web:systems_no_thirdparty_dependencies_diagram'))],
                    children=res)
