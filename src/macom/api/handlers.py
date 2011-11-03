# -*- coding: UTF-8 -*-
from piston.handler import BaseHandler
from macom.diagrama.models import System, Module, Interface, Dependency
from django.core.urlresolvers import reverse
from django.template.context import Context
from django.conf import settings 

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
            syst['kind'] = "system"
            syst['resource_uri'] = reverse('api_system', args=[syst['id']])
            syst['full_name']  = syst['name']
            syst_id = syst['id']
            syst['id'] = "%s%s" % (syst['kind'], syst_id)
            res.append(syst)
            modus = []
            for modu in Module.objects.filter(system__id=syst_id).values('id', 'name'):
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
                    inte['id'] = "%s%s" % (inte['kind'],inte['id'])
                    intes.append(inte)
                modu['children'] = intes
            syst['children'] = modus
        return {'kind': 'root', 
                        'name' : 'Sistema',
                        'full_name':'Sistema',
                        'resource_uri': 'root',
                        'isOpen': 'true',
                        'diagrams' : ( { 'name': 'Sistemas con dependencias',
                                                      'resource_uri': self.getUrl('web:systems_dependencies_diagram', request)  },
                                                  { 'name': 'Sistemas sin dependencias externas',
                                                     'resource_uri': self.getUrl('web:systems_no_thirdparty_dependencies_diagram', request) } ),
                        'children' : res }
        
    def getUrl(self, url, request):
        return  "%s/%s" % (settings.DIAGRAM_SERVICE_URL, request.build_absolute_uri(reverse(url)))
