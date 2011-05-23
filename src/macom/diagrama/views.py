# -*- coding: utf-8 -*-

'''
Created on 09/03/2011

@author: sebas
'''

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response
from pydot import graph_from_dot_data
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from diagrama.utils import RawGraphViz, Utils

def root(request):
    '''
        Sólo redirecciona a filter.  Está para permitir un acceso más directo a la aplicación.
    '''
    return HttpResponseRedirect(reverse(filter))

def filter(request, format="", view="", show="", minimized="", related=""):
    req = request.REQUEST
    if request.method == 'GET':
        ctx = Utils.context(format, view, show, minimized, related)
        ctx.update(csrf(request))
        
        if view == 'completo':
            g = RawGraphViz(show, minimized, related, extra={'layout': 'fdp', 'size': '10'}).graph()
            request.session['program'] = None
        else:
            g = Utils.plantUML(Utils.split(show, '_'))
            request.session['program'] = 'fdp'
    
        ctx['cmap'] = g.create(format='cmapx') if g is not None else None
        request.session['graph'] = g.to_string() if g is not None else None

        return render_to_response('filter.html', ctx)
    else:
        return HttpResponseRedirect(reverse(filter, kwargs=Utils.request_to_context(req)))

def show(request, format='png'):
    '''
        Espera encontrar en la session un gráfico graphviz y lo renderiza
        en el formato recibido como parámetro.
    '''
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    
    if format not in Utils.CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    program = request.session['program']
    g = graph_from_dot_data(request.session['graph'])
    response = HttpResponse(g.create(program, format=format), content_type=Utils.CONTENT_TYPES[format])
    response['Cache-Control'] = 'no-cache'
    return response

def download(request, format="png", view="", show="", minimized="", related=""):
    '''
        Regenera el gráfico y lo devuelve según el formato que recibe como parámetro.
    '''
    if format not in Utils.CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    show = Utils.split(show, "_")
    program = None
    if view == 'completo':
        g = RawGraphViz(show, Utils.split(minimized, "_"), Utils.split(related, "_"), extra={'layout': 'fdp'}).graph()
    else:
        g = Utils.plantUML(show)
        program = 'fdp'
            
    return HttpResponse(g.create(program, format=format), content_type=Utils.CONTENT_TYPES[format])
