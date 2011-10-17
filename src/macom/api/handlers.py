'''
Created on 06/10/2011

@author: plalloni
'''
from piston.handler import BaseHandler
from macom.diagrama.models import System, Module, Interface
from django.core.urlresolvers import reverse

class SystemHandler(BaseHandler):
    model = System

class ModuleHandler(BaseHandler):
    model = Module

class InterfaceHandler(BaseHandler):
    model = Interface
    
class ModelHandler(BaseHandler):
    def read(self, request):
        res = []
        for syst in System.objects.values('id', 'name'):
            syst['type'] = "system"
            syst['readurl'] = reverse('api_system', args=[syst['id']])
            res.append(syst)
            modus = []
            for modu in Module.objects.filter(system__id=syst['id']).values('id', 'name'):
                modu['type'] = "module"
                modu['readurl'] = reverse('api_module', args=[modu['id']])
                modus.append(modu)
                intes = [] 
                for inte in Interface.objects.filter(module__id=modu['id']).values('id', 'name'):
                    inte['type'] = "interface"
                    inte['readurl'] = reverse('api_interface', args=[inte['id']])
                    intes.append(inte)
                modu['children'] = intes
            syst['children'] = modus
        return res
