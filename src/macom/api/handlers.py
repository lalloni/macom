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

class SystemHandler(Defaults):
    model = System
    fields = ('kind', 'name', 'full_name', 'external', 'description', 'referents', 'documentation', ('modules', ()), 'dependents', 'dependencies', 'diagram_uri')
    @classmethod
    def dependents(cls, system):
        return Dependency.objects.filter(interface__module__system=system).exclude(module__system=system)
    @classmethod
    def dependencies(cls, system):
        return Dependency.objects.filter(module__system=system).exclude(interface__module__system=system)
        
class ModuleHandler(Defaults):
    model = Module
    fields = ('kind', 'name', 'full_name', 'external', 'goal', 'referents', 'documentation', ('interfaces', ()), 'dependencies', 'diagram_uri')
    @classmethod
    def dependencies(cls, module):
        return module.dependency_objects()

class InterfaceHandler(Defaults):
    model = Interface
    fields = ('kind', 'name', 'full_name', 'goal', 'referents', 'documentation', 'technology', 'direction', 'diagram_uri')

class DependencyHandler(Defaults):
    model = Dependency
    fields = ('kind', 'name', 'full_name', 'goal', 'referents', 'documentation', 'technology', 'direction', 'loadestimate', 'interface')
    
class ModelHandler(BaseHandler):
    def read(self, request):
        res = []
        for syst in System.objects.values('id', 'name'):
            syst['type'] = "system"
            syst['nid'] = syst['id']
            syst['id'] = syst['type'] + str(syst['id'])
            syst['readurl'] = reverse('api_system', args=[syst['nid']])
            res.append(syst)
            modus = []
            for modu in Module.objects.filter(system__id=syst['nid']).values('id', 'name'):
                modu['type'] = "module"
                modu['nid'] = modu['id']
                modu['id'] = modu['type'] + str(modu['id'])
                modu['readurl'] = reverse('api_module', args=[modu['nid']])
                modus.append(modu)
                intes = [] 
                for inte in Interface.objects.filter(module__id=modu['nid']).values('id', 'name'):
                    inte['type'] = "interface"
                    inte['nid'] = inte['id']
                    inte['id'] = inte['type'] + str(inte['id'])
                    inte['readurl'] = reverse('api_interface', args=[inte['nid']])
                    intes.append(inte)
                modu['children'] = intes
            syst['children'] = modus
        return res
