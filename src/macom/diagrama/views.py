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
    g = graph('systems', minimized, closed, extra={'layout': 'fdp', 'size': '10'})
    systems_count = len(System.objects.all())
    ctx = {
           'cmap': g.create(format='cmapx'), 
           'mapname': 'systems', 
           'show_maximizeall': len(minimized) > 0, 
           'show_openall': len(closed) > 0,
           'show_minimizeall': len(minimized) != systems_count, 
           'show_closeall': len(closed) != systems_count
    }
    request.session['graph'] = g.to_string()
    
    return render_to_response("detail.html", ctx)

def png(request):
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    
    str_g = request.session['graph']
    g = graph_from_dot_data(str_g)

    response = HttpResponse(g.create(format='png'), content_type='image/png')
    response['Cache-Control'] = 'no-cache'
    return response

def download(request, size = '100'):
    minimized = request.session.get('minimized', {})
    closed = request.session.get('closed', {})
    g = graph('systems', minimized, closed, extra={'layout': 'fdp', 'size': str(size)}, cleaned=True)
    return HttpResponse(g.create(format='svg'), content_type='image/svg+xml')
    #return HttpResponse(g.create(format='png'), content_type='image/png')
    #return HttpResponse(g.create(format='ps'), content_type='application/postscript')
