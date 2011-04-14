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
from diagrama.models import System

CONTENT_TYPES = {
     'png': 'image/png',
     'svg': 'image/svg+xml',
     'ps': 'application/postscript'
}

def show_related_systems(request):
    request.session['show_related_systems'] = True
    return HttpResponseRedirect(reverse(detail))

def hide_related_systems(request):
    request.session['show_related_systems'] = False
    return HttpResponseRedirect(reverse(detail))

def maximize_all(request):
    request.session['minimized'] = []
    return HttpResponseRedirect(reverse(detail))

def minimize_all(request):
    minimized = request.session.get('minimized', [])
    if type(minimized).__name__ != 'list':
        minimized = []
    minimized.extend([str(s.id) for s in System.objects.order_by('id').all()])
    request.session['minimized'] = minimized
    return HttpResponseRedirect(reverse(detail))

def close_all(request):
    closed = request.session.get('closed', [])
    closed.extend([str(s.id) for s in System.objects.order_by('id').all()])
    request.session['closed'] = closed
    return HttpResponseRedirect(reverse(detail))

def open_all(request):
    request.session['closed'] = []

    return HttpResponseRedirect(reverse(detail))

def close(request, id):
    closed = request.session.get('closed', [])
    closed.append(str(id))
    request.session['closed'] = closed

    return HttpResponseRedirect(reverse(detail))

def minimize(request, id):
    minimized = request.session.get('minimized', [])
    minimized.append(str(id))
    request.session['minimized'] = minimized

    return HttpResponseRedirect(reverse(detail))

def maximize(request, id):
    minimized = request.session.get('minimized', [])
    if str(id) in minimized:
        minimized.remove(str(id))
        request.session['minimized'] = minimized

    return HttpResponseRedirect(reverse(detail))
    
def open(request, id):
    closed = request.session.get('closed', [])
    if str(id) in closed:
        closed.remove(str(id))
        request.session['closed'] = closed

    return HttpResponseRedirect(reverse(detail))

def detail(request):
    minimized = request.session.get('minimized', [])
    closed = request.session.get('closed', [])
    show_related_systems = request.session.get('show_related_systems', False)
    g = graph('systems', minimized, closed, extra={'layout': 'fdp', 'size': '10'}, show_related_systems=show_related_systems)
    systems_count = len(System.objects.all())
    ctx = {
           'cmap': g.create(format='cmapx'),
           'mapname': 'systems',
           'show_maximizeall': len(minimized) > 0,
           'show_openall': len(closed) > 0,
           'show_minimizeall': len(minimized) != systems_count,
           'show_closeall': len(closed) != systems_count,
           'show_related_systems_enabled': show_related_systems
    }
    request.session['graph'] = g.to_string()
    
    return render_to_response("detail.html", ctx)

def show(request, format='png'):
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    
    if format not in CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    g = graph_from_dot_data(request.session['graph'])
    response = HttpResponse(g.create(format=format), content_type=CONTENT_TYPES[format])
    response['Cache-Control'] = 'no-cache'
    return response

def download(request, size='100', format='png'):
    if format not in CONTENT_TYPES:
        return HttpResponseNotFound("Content type '%s' not supported" % format)
    
    minimized = request.session.get('minimized', {})
    closed = request.session.get('closed', {})
    show_related_systems = request.session.get('show_related_systems', False)
    g = graph('systems', minimized, closed, extra={'layout': 'fdp', 'size': str(size)}, cleaned=True, show_related_systems=show_related_systems)

    return HttpResponse(g.create(format=format), content_type=CONTENT_TYPES[format])
