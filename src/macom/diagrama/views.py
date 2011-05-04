# -*- coding: utf-8 -*-

'''
Created on 09/03/2011

@author: sebas
'''

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response
from diagrama.utils import graph
from pydot import graph_from_dot_data
from django.core.urlresolvers import reverse
from diagrama.models import System, Interface
from django import forms
from django.core.context_processors import csrf

CONTENT_TYPES = {
     'png': 'image/png',
     'svg': 'image/svg+xml',
     'ps': 'application/postscript'
}

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
def root(request):
    '''
        Sólo redirecciona a filter.  Está para permitir un acceso más directo a la aplicación.
    '''
    return HttpResponseRedirect(reverse(filter))

def filter(request, format="", show="", minimized="", related=""):
    ctx = {}
    ctx.update(csrf(request))
    
    req = request.REQUEST
    if request.method == 'GET':
        ctx['format'] = format if format else CONTENT_TYPES.keys()[0]
        ctx['show'] = show
        ctx['minimized'] = minimized
        ctx['related'] = related
        ctx['contenttypes'] = CONTENT_TYPES.keys()
        
        show = __split(show, "_")
        minimized = __split(minimized, "_")
        related = __split(related, "_")
        ctx['systems'] = list()
        for s in System.objects.order_by('name').all():
            obj = {
                   'id': s.id, 
                   'name': s.name, 
                   'show': str(s.id) in show,
                   'minimized': str(s.id) in minimized,
                   'related': str(s.id) in related
            }
            ctx['systems'].append(obj)
            
        g = __graph(show, minimized, related, extra={'layout': 'fdp', 'size': '10'})
        
        ctx['empty'] = len(show) == 0
        ctx['cmap'] = g.create(format='cmapx')
        ctx['mapname'] = 'systems'

        request.session['graph'] = g.to_string()

        return render_to_response('filter.html', ctx)
    else:
        show, minimized, related = [], [], []
        for k in req.keys():
            __add_if_starts_with('show', k, show)
            __add_if_starts_with('minimized', k, minimized)
            __add_if_starts_with('related', k, related)

        args = {
            'format': req.get('formato') if req.get('formato') else CONTENT_TYPES.keys()[0],
            'show': __serialize(show),         
            'minimized': __serialize(minimized),
            'related': __serialize(related),
        }

        return HttpResponseRedirect(reverse(filter, kwargs=args))

def show(request, format='png'):
    '''
        Espera encontrar en la session un gráfico graphviz y lo renderiza
        en el formato recibido como parámetro.
    '''
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    
    if format not in CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    g = graph_from_dot_data(request.session['graph'])
    response = HttpResponse(g.create(format=format), content_type=CONTENT_TYPES[format])
    response['Cache-Control'] = 'no-cache'
    return response

def download(request, format="png" , show="", minimized="", related=""):
    '''
        Regenera el gráfico y lo devuelve según el formato que recibe como parámetro.
    '''
    if format not in CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    g = __graph(__split(show, "_"), __split(minimized, "_"), __split(related, "_"), extra={'layout': 'fdp'})

    return HttpResponse(g.create(format=format), content_type=CONTENT_TYPES[format])

def __serialize(objs, sep="_"):
    return sep.join(objs)

def __split(value, char=","):
    list = value.split(char) if str(value) is not "" and str(value) is not None else []
    return map(lambda x: x.strip(), list)

def __add_if_starts_with(prefix, value, objs):
    if value.startswith(prefix):
        objs.append(value[len(prefix)+1:])

def __graph(show, minimized, related, extra={}):
    systems = System.objects.order_by('id').all()
    related_systems = dict()
    by_id = dict()
    
    for s in systems:
        related_systems[str(s.id)] = list(set(map(lambda i: i.exposer.system, Interface.objects.filter(consumers__system__id=s.id))))
        related_systems[str(s.id)].extend(list(set(map(lambda i: i.exposer.system, Interface.objects.filter(exposer__system__id=s.id)))))
        by_id[str(s.id)] = s

    to_show = set()
    to_minimize = set()
    for s in show:
        to_show.add(by_id[str(s)])
    for s in minimized:
        to_minimize.add(by_id[str(s)])
    for s in related:
        to_show = to_show.union(related_systems[str(s)])
        
    return graph('systems', show=to_show, minimized=to_minimize, extra=extra)
