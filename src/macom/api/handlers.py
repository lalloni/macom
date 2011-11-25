# -*- coding: UTF-8 -*-
from piston.handler import BaseHandler
from macom.diagrama.models import System, Module, Interface, Dependency
from django.core.urlresolvers import reverse

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

class SystemHandler(Defaults):
    model = System
    fields = ('kind', 'name', 'full_name', 'external', 'description', 'functional_referents', 'implementation_referents', 'documentation', ('modules', ('kind', 'name')), 'dependencies', 'reverse_dependencies', 'diagram_uri')
    @classmethod
    def reverse_dependencies(cls, system):
        return map(cls.short_of, Dependency.objects.filter(interface__module__system=system).exclude(module__system=system))
    @classmethod
    def dependencies(cls, system):
        return cls.resource_uri_of(system) + '/dependencies'

class ModuleHandler(Defaults):
    model = Module
    fields = ('kind', 'name', 'full_name', 'external', 'goal', ('system', ('kind', 'name')), 'functional_referents', 'implementation_referents', 'documentation', ('interfaces', ('kind', 'name')), 'dependencies', 'reverse_dependencies', 'diagram_uri')
    @classmethod
    def dependencies(cls, module):
        return map(cls.short_of, module.dependency_objects())

class InterfaceHandler(Defaults):
    model = Interface
    fields = ('kind', 'name', 'full_name', 'goal', ('module', ('kind', 'name', ('system', ('kind', 'name')))), 'published', 'technology', 'direction', 'functional_referents', 'implementation_referents', 'documentation', 'reverse_dependencies', 'diagram_uri')
    @classmethod
    def read(cls, req, interface=None, system=None, module=None):
        if interface:
            return Interface.objects.get(id=interface)
        if module:
            return Interface.objects.filter(module=module)
        if system:
            return Interface.objects.filter(module__system=system, published=True)
        else:
            return Interface.objects.all()

class DependencyHandler(Defaults):
    model = Dependency
    fields = ('kind', 'name', 'full_name', 'goal', ('module', ('kind', 'name', ('system', ('kind', 'name')))), 'functional_referents', 'implementation_referents', 'documentation', 'technology', 'direction', 'loadestimate', ('interface', ('kind', 'name', ('module', ('kind', 'name', ('system', ('kind', 'name')))))))
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
                    diagrams=[dict(name='Dependencias entre sistemas', diagram_uri=reverse('web:systems_dependencies_diagram')),
                              dict(name='Dependencias entre sistemas (excluyendo externos)', diagram_uri=reverse('web:systems_no_thirdparty_dependencies_diagram'))],
                    children=res)
