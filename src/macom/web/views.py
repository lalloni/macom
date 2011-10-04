# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response
#from pydot import graph_from_dot_data
from django.core.urlresolvers import reverse
#from django.core.context_processors import csrf
from diagrama.models import *
    
def index(request):
    return HttpResponseRedirect(reverse(system))
                                
def system(request):
    items = System.objects.all()
    return render_to_response('systems.html', 
                                {'systemlist': items,}
                                )

def systemdetail(request, id=-1):
    systemlist = System.objects.filter( id=id )
    modules = Module.objects.filter( system = id )
    return render_to_response('systemdetail.html', 
                                {'systemlist': systemlist,'systemmodules': modules }
                                )

def module(request):
    items = Module.objects.all()
    return render_to_response('modules.html', 
                                {'modulelist': items,}
                                )

def moduledetail(request, id=-1):
    modulelist = Module.objects.filter( id = id )
    interfaces = Dependency.objects.filter( exposer=id )
    
    return render_to_response('moduledetail.html', 
                                {'modulelist': modulelist,'dependencies': interfaces }
                                )