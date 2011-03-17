# -*- coding: utf-8 -*-

'''
Created on 09/03/2011

@author: sebas
'''

from django.http import HttpResponse, HttpResponseNotFound
from macom.diagrama.models import System, Module, Interface
from django.shortcuts import render_to_response
from diagrama.utils import graph
from pydot import graph_from_dot_data

def system_detail(request, id):
    return render_to_response('system-detail.html', {'object': System.objects.get(id=id)})

def module_detail(request, id):
    return render_to_response('module-detail.html', {'object': Module.objects.get(id=id)})

def interface_detail(request, id):
    return render_to_response('interface-detail.html', {'object': Interface.objects.get(id=id)})
        
def detail(request):
    g = graph('systems', {'layout': 'fdp', 'size': '10'})
    ctx = {'cmap': g.create(format='cmapx'), 'mapname': 'systems'}
    
    request.session['graph'] = g.to_string()
    
    return render_to_response("detail.html", ctx)

def png(request):
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    g = graph_from_dot_data(request.session['graph'])
    return HttpResponse(g.create(format='png'), content_type='image/png')

def download(request, size = '100'):
    g = graph('systems', {'layout': 'fdp', 'size': str(size)})
    return HttpResponse(g.create(format='png'), content_type='image/png')
