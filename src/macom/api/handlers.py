'''
Created on 06/10/2011

@author: plalloni
'''
from piston.handler import BaseHandler
from macom.diagrama.models import System

class SystemHandler(BaseHandler):
    model = System
