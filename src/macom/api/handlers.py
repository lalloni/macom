'''
Created on 06/10/2011

@author: plalloni
'''
from piston.handler import BaseHandler
from macom.diagrama.models import System, Module, Interface

class SystemHandler(BaseHandler):
    model = System

class ModelHandler(BaseHandler):
    def read(self, request):
        res = []
        for syst in System.objects.values('id', 'name'):
            syst['type'] = "system"
            res.append(syst)
            modus = []
            for modu in Module.objects.filter(system__id=syst['id']).values('id', 'name'):
                modu['type'] = "module"
                modus.append(modu)
                intes = [] 
                for inte in Interface.objects.filter(module__id=modu['id']).values('id', 'name'):
                    inte['type'] = "interface"
                    intes.append(inte)
                modu['children'] = intes
            syst['children'] = modus
        return res
