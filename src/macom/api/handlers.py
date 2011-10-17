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
