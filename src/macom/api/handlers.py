'''
Created on 06/10/2011

@author: plalloni
'''
from piston.handler import BaseHandler
from macom.diagrama.models import System, Module, Interface, Dependency
from django.core.urlresolvers import reverse

class Defaults(BaseHandler):
    allowed_methods = ('GET',)
    @classmethod
    def kind(cls, m):
        return cls.model._meta.object_name.lower()
    @classmethod
    def full_name(cls, m):
        return unicode(m)

class SystemHandler(Defaults):
    model = System
    fields = ('kind', 'absolute_uri', 'name', 'full_name', 'external', 'description', 'referents', 'documentation', ('modules', ()))
    
class ModuleHandler(Defaults):
    allowed_methods = ('GET',)
    model = Module
    fields = ('kind', 'absolute_uri', 'name', 'full_name', 'external', 'goal', 'referents', 'documentation', ('interfaces', ()), 'dependencies')
    @classmethod
    def dependencies(cls, module):
        return module.dependency_objects()

class InterfaceHandler(Defaults):
    allowed_methods = ('GET',)
    model = Interface
    fields = ('kind', 'absolute_uri', 'name', 'full_name', 'goal', 'referents', 'documentation', 'technology', 'direction')
    @classmethod
    def direction(cls, interface):
        return interface.direction() 

class DependencyHandler(Defaults):
    allowed_methods = ('GET',)
    model = Dependency
    fields = ('kind', 'absolute_uri', 'name', 'full_name', 'goal', 'referents', 'documentation', 'technology', 'direction', 'loadestimate', 'interface')
    @classmethod
    def direction(cls, dep):
        return dep.direction() 
    
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
